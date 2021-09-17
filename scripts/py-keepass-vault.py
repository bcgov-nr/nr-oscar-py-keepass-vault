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

# read KeePass entries
fullList = kp.entries

# loading vault url and token
client = hvac.Client(ENV_VAULT_ADDR)
client.token = ENV_VAULT_TOKEN

# pushing KeePass entries to vault
# create a new v2 secrets engine using vault ui and set it as mount point
for entry in fullList:
    try:
        create_response = client.secrets.kv.v2.create_or_update_secret(mount_point=ENV_MOUNT_POINT, path=ENV_SECRETS_PATH+'/'+entry.title, secret=dict(title=entry.title, username=entry.username, password=entry.password, notes=entry.notes))
    except Exception as error:
        print (error.args)