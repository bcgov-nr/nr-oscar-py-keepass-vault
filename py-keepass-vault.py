from pykeepass import PyKeePass
import hvac
import os

# load database
kp = PyKeePass(os.environ['KEEPASS_PATH'], password=os.environ['KEEPASS_PWD'])

# read KeePass entries
fullList = kp.entries

# loading vault url and token
client = hvac.Client(url=os.environ['VAULT_ADDR'])
client.token = os.environ['VAULT_TOKEN']

# pushing KeePass entries to vault
# create a new v2 secrets engine using vault ui and set it as mount point
for entry in fullList:
    create_response = client.secrets.kv.v2.create_or_update_secret(mount_point=os.environ['MOUNT_POINT'], path=entry.title, secret=dict(title=entry.title, username=entry.username, password=entry.password, notes=entry.notes))
