from pykeepass import PyKeePass
import hvac
import os

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
        custom_metadata={
            "keepass_title": entry.title,
            "keepass_filename": kfile,
            "keepass_uuid": entry.uuid.hex,
            "keepass_url": entry.url if entry.url else None,
            "keepass_notes": entry.notes if entry.notes else None
        }
        custom_metadata = {key: value for key, value in custom_metadata.items() if value is not None}

        client.secrets.kv.v2.update_metadata(
            path=ENV_SECRETS_PATH+'/'+ (str(entry.group).split())[1].split('"')[1] + '/' +entry.title.replace("/","_"),
            custom_metadata=custom_metadata
        )
        print((str(entry.group).split())[1].split('"')[1])
    except Exception as error:
        print (error.args)