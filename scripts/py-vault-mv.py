import hvac
import json
import os
import argparse

# read environment variables
ENV_VAULT_ADDR = os.environ['VAULT_ADDR']
ENV_VAULT_TOKEN = os.environ['VAULT_TOKEN']
ENV_MOUNT_POINT = os.environ['MOUNT_POINT']
ENV_SECRETS_PATH = os.environ['MV_SECRETS_PATH']
ENV_NEW_SECRETS_PATH = os.environ['NEW_SECRETS_PATH']

if ENV_NEW_SECRETS_PATH.startswith(ENV_SECRETS_PATH):
    exit("ERROR: Cannot move secrets to a sub-path of the source. This causes an infinite loop.")

# parse arguments
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description='''\
Copy Vault secrets from a source path to a target path.

Uses the following environment variable configuration:
    VAULT_ADDR: address of the Vault instance (ex. http://localhost:8200)
    VAULT_TOKEN: user api token used to authenticate with Vault
    MOUNT_POINT: mount point where the secrets are stored
    MV_SECRETS_PATH: path to copy secrets from
    NEW_SECRETS_PATH: path to copy secrets to
                               ''')
parser.add_argument('--copy-all-versions',
                    help="Copy all versions of the source path to the target path.",
                    action='store_true',
                    default=False)

args = parser.parse_args()


# load vault url and token
client = hvac.Client(url=ENV_VAULT_ADDR,
                     token=ENV_VAULT_TOKEN)

if not client.is_authenticated():
    exit("Unable to authenticate Vault client at " + ENV_VAULT_ADDR + " with the given VAULT_TOKEN.")


def get_vault_paths(path):
    try:
        return client.secrets.kv.v2.list_secrets(mount_point=ENV_MOUNT_POINT,
                                             path=path)["data"]["keys"]
    except hvac.exceptions.InvalidPath as error:
        return None


def get_current_valid_version(current_version, versions):
    print("Current_Version: ")
    print(current_version)
    print(versions)
    valid_version = 0
    version_count = current_version
    while version_count > 0:
        print(versions[str(version_count)])
        if str(version_count) in list(versions.keys()) and not (versions[str(version_count)]["destroyed"] or versions[str(version_count)]["deletion_time"]):
            valid_version = version_count
            break
        version_count -= 1
    return valid_version


def move_vault_path_dryrun(old_path, new_path):
    # recursively check for conflicts which would occur when moving old_path to new_path
    #
    # return a dictionary of {conflicting_path: <list>, old_path: <list>, new_path: <list>} 
    vault_paths = get_vault_paths(old_path)
    
    dryrun = {"conflicting_path": [], "old_path": [], "new_path": []}

    for path in vault_paths or []:
        # recurse paths
        if path.endswith("/"):
            path = path.rstrip("/")
            dryrun["conflicting_path"].extend(move_vault_path_dryrun(old_path="/".join([old_path, path]),
                                                                      new_path="/".join([new_path, path])))

        # check secrets for conflicts
        else:
            target_path = "/".join([new_path, path])
           
            dryrun["old_path"].extend(["/".join([old_path, path])])
            dryrun["new_path"].extend([target_path])

            try:
                # check for key conflict
                # raise_on_deleted_version: see https://github.com/hvac/hvac/pull/907
                maybe_conflict = client.secrets.kv.v2.read_secret_version(mount_point=ENV_MOUNT_POINT,
                                                                          path=target_path,
                                                                          raise_on_deleted_version=True)
            except hvac.exceptions.InvalidPath as error:
                # there is no key conflict
                maybe_conflict = None

            if maybe_conflict:
                dryrun["conflicting_path"].extend([target_path])
    
    return dryrun


def copy_vault_path(old_path, new_path):
    # recursively copy all old_path to new_path
    # copies metadata and optionally all versions
    # does not copy deleted or destroyed versions
    #
    # return a dictionary of {old_path: <list>, new_path: <list>} of copied paths
    vault_paths = get_vault_paths(old_path)

    copied_paths = {"old_path":[], "new_path":[]}

    for path in vault_paths:
        # recurse paths
        if path.endswith("/"):
            path = path.rstrip("/")
            recursively_copied_paths = copy_vault_path(old_path="/".join([old_path, path]),
                                                       new_path="/".join([new_path, path]))

            copied_paths["old_path"].extend(recursively_copied_paths["old_path"])
            copied_paths["new_path"].extend(recursively_copied_paths["new_path"])

        # copy to new path
        else:
            source_path = "/".join([old_path, path])
            target_path = "/".join([new_path, path])

            print("Copy source: " + source_path)
            print("Copy target: " + target_path)

            # get the versions 
            source_secret_metadata = client.secrets.kv.v2.read_secret_metadata(mount_point=ENV_MOUNT_POINT,
                                                                               path=source_path)
            
            # copy each version to the target
            if args.copy_all_versions:
                current_version = 0
                for version, version_metadata in source_secret_metadata["data"]["versions"].items():
                    # skip destroyed/deleted versions
                    if version_metadata["destroyed"] or version_metadata["deletion_time"]:
                        continue

                    # raise_on_deleted_version: see https://github.com/hvac/hvac/pull/907
                    source_secret = client.secrets.kv.v2.read_secret_version(mount_point=ENV_MOUNT_POINT,
                                                                             path=source_path,
                                                                             version=version,
                                                                             raise_on_deleted_version=True)

                    copy_response = client.secrets.kv.v2.create_or_update_secret(mount_point=ENV_MOUNT_POINT,
                                                                                 path=target_path,
                                                                                 secret=source_secret["data"]["data"],
                                                                                 cas=current_version)
                    current_version += 1

                # when no version is copied, skip to next path
                if current_version <= 0:
                    print("No valid version. Did not copy " + source_path)
                    continue

            # copy only the latest version
            else:
                valid_version = get_current_valid_version(source_secret_metadata["data"]["current_version"], source_secret_metadata["data"]["versions"])
                if valid_version <= 0:
                    print("No valid version. Did not copy " + source_path)
                    continue

                try:
                    # raise_on_deleted_version: see https://github/comhvac/hvac/pull/907
                    source_secret = client.secrets.kv.v2.read_secret_version(mount_point=ENV_MOUNT_POINT,
                                                                             path=source_path,
                                                                             version=valid_version,
                                                                             raise_on_deleted_version=True)

                except hvac.exceptions.InvalidPath as error:
                    # this is unexpected because get_current_valid_version should only return valid_version >0 for secrets that can be read
                    print("An unexpected error occurred. Did not copy " + source_path) 

                copy_response = client.secrets.kv.v2.create_or_update_secret(mount_point=ENV_MOUNT_POINT,
                                                                             path=target_path,
                                                                             secret=source_secret["data"]["data"],
                                                                             cas=0)

            # copy the metadata
            metadata_response = client.secrets.kv.v2.update_metadata(mount_point=ENV_MOUNT_POINT,
                                                                     path=target_path,
                                                                     custom_metadata=source_secret_metadata["data"]["custom_metadata"])
            
            copied_paths["old_path"].extend(source_path)
            copied_paths["new_path"].extend(target_path)

    return copied_paths


def move_vault_path(old_path, new_path):
    # move all Vault paths listed under old_path to new_path
    # if any entries conflict at new_path, abort
    # otherwise, print dryrun and request confirmation to copy
    # put new entries in new_path, preserving versions and metadata
   
    dryrun = move_vault_path_dryrun(old_path, new_path)
    
    # print any conflicts and exit
    if dryrun["conflicting_path"]:
        print("Refused to move secrets because the following paths would be overwritten:")
        for conflict in dryrun["conflicting_path"]:
            print(conflict)
        exit("Unable to move secrets to " + new_path + " due to conflicting paths.")

    elif not (dryrun["old_path"] and dryrun["new_path"]):
        print("There were no secrets found to be moved at " + old_path)
        exit("There is nothing to copy.")

    # no conflicts, print dryrun results
    else:
        for source_path, target_path in zip(dryrun["old_path"], dryrun["new_path"]):
            print("Preparing to copy source: " + source_path)
            print("Preparing to copy target: " + target_path)

    # confirm copy after dry run
    yes_choices = ["yes", "y"]
    no_choices = ["no", "n"]
    print("\nNo conflicts detected.\n")
    while True:
        user_input = input("Do you want to continue copying? yes/no: ")
        if user_input.lower() in yes_choices:
            break
        elif user_input.lower() in no_choices:
            exit("Did not copy secrets.")
        else:
            print("Type 'yes'/'y'/'no'/'n'")

    copied = copy_vault_path(old_path, new_path)

    return

#####
# Do the move.
#####
move_vault_path(ENV_SECRETS_PATH, ENV_NEW_SECRETS_PATH)

