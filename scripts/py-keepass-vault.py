from pykeepass import PyKeePass
import hvac
import os
import sys

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
        create_response = client.secrets.kv.v2.create_or_update_secret(mount_point=ENV_MOUNT_POINT, path=ENV_SECRETS_PATH+'/'+ (str(entry.group).split())[1].split('"')[1]+ '/' +entry.title.replace("/","_"), secret=dict(username=entry.username, password=entry.password))
        client.secrets.kv.v2.update_metadata(
            path=ENV_SECRETS_PATH+'/'+ (str(entry.group).split())[1].split('"')[1] + '/' +entry.title.replace("/","_"),
            cas_required=True,
            custom_metadata={
                "keepass-title": entry.title,
                "keepass-file": kfile,
                "keepass-uuid": str(entry.uuid),
                "keepass-url": entry.url,
                "keepass-notes": entry.notes
            }
        )
        print((str(entry.group).split())[1].split('"')[1])
    except Exception as error:
        print (error.args)