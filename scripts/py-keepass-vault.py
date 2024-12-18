from pykeepass import PyKeePass
import hvac
import os
import urllib.parse

# reading environment variables
ENV_KEEPASS_PATH = os.environ['KEEPASS_PATH']
ENV_KEEPASS_PWD = os.environ['KEEPASS_PWD']
ENV_VAULT_ADDR = os.environ['VAULT_ADDR']
ENV_VAULT_TOKEN = os.environ['VAULT_TOKEN']
ENV_MOUNT_POINT = os.environ['MOUNT_POINT']
ENV_SECRETS_PATH = os.environ['SECRETS_PATH']

# load database
kp = PyKeePass(ENV_KEEPASS_PATH, password=ENV_KEEPASS_PWD)
kfile = os.path.basename(ENV_KEEPASS_PATH)

# read KeePass entries
fullList = kp.entries

# loading vault url and token
client = hvac.Client(ENV_VAULT_ADDR)
client.token = ENV_VAULT_TOKEN

# pushing KeePass entries to vault
# create a new v2 secrets engine using vault ui and set it as mount point
for entry in fullList:
    try:
        coerced_entry_group = ('' if entry.group.is_root_group else '/'+str(entry.group).split('"')[1])
        entry_path = ENV_SECRETS_PATH+coerced_entry_group+'/'+entry.title.replace("/","_")+'-'+entry.uuid.hex

        if entry.notes and entry.notes.lower().find('moved to vault') >= 0:
            print("Skipping, previously moved to vault: " + entry_path)
            continue

        print("Creating: " + entry_path)

        create_response = client.secrets.kv.v2.create_or_update_secret(
                mount_point=ENV_MOUNT_POINT,
                path=entry_path,
                secret=dict(username=entry.username, password=entry.password))

        print("Updating metadata.")
        custom_metadata={
            "keepass_title": entry.title,
            "keepass_filename": kfile,
            "keepass_uuid": entry.uuid.hex,
            "keepass_url": entry.url if entry.url else None,
        }
        custom_metadata = {key: value for key, value in custom_metadata.items() if value is not None}

        client.secrets.kv.v2.update_metadata(
            mount_point=ENV_MOUNT_POINT,
            path=entry_path,
            custom_metadata=custom_metadata
        ) 

        print("Writing URL to KeePass file.")
        vault_url = ENV_VAULT_ADDR+"/ui/vault/secrets/"+ENV_MOUNT_POINT+"/kv/"+urllib.parse.quote(entry_path, safe='')+"/details"
        entry.notes = "Vault URL: "+vault_url+"\n\n"+(entry.notes if entry.notes else '')


    except Exception as error:
        print (error.args)

kp.save()
