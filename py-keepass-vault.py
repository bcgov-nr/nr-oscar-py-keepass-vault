from pykeepass import PyKeePass
import hvac
import os
import sys

# load database
#kp = PyKeePass(os.getenv('KEEPASS_PATH','test'), password=os.getenv('KEEPASS_PWD','test'))
ENV_KEEPASS_PATH = os.environ['KEEPASS_PATH']
ENV_KEEPASS_PWD = os.environ['KEEPASS_PWD']
ENV_VAULT_ADDR = os.environ['VAULT_ADDR']
ENV_VAULT_TOKEN = os.environ['VAULT_TOKEN']
ENV_MOUNT_POINT = os.environ['MOUNT_POINT']
ENV_SECRETS_PATH = os.environ['SECRETS_PATH']




#ENV_KEEPASS_PATH = 'sample.kdbx'
ENV_KEEPASS_PWD = '12345678'
# ENV_VAULT_ADDR = 'https://vault-iit-dev.apps.silver.devops.gov.bc.ca/'
#ENV_VAULT_TOKEN = 's.OCiaMT20TJap1z7rYOdyffpW'
# ENV_MOUNT_POINT = 'user'
# ENV_SECRETS_PATH = 'sanjay.babu@gov.bc.ca/test-load7'





kp = PyKeePass(ENV_KEEPASS_PATH, password=ENV_KEEPASS_PWD)

#kp = PyKeePass(os.environ['KEEPASS_PATH'], password=os.environ['KEEPASS_PWD'])

# read KeePass entries
fullList = kp.entries

# loading vault url and token
# client = hvac.Client(url=os.environ['VAULT_ADDR'])
# client.token = os.environ['VAULT_TOKEN']



client = hvac.Client(ENV_VAULT_ADDR)
client.token = ENV_VAULT_TOKEN


# writing log
#old_stdout = sys.stdout

#log_file = open("message.log","w")

#sys.stdout = log_file

print ("this will be written to message.log")

#print (os.environ['PWD'])




# pushing KeePass entries to vault
# create a new v2 secrets engine using vault ui and set it as mount point
# for entry in fullList:
#     try:
#         create_response = client.secrets.kv.v2.create_or_update_secret(mount_point=os.environ['MOUNT_POINT'], path=os.environ['SECRETS_PATH']+'/'+entry.title, secret=dict(title=entry.title, username=entry.username, password=entry.password, notes=entry.notes))
#     except Exception as error:
#         print (error.args)


# for entry in fullList:
#     try:
#         create_response = client.secrets.kv.v2.create_or_update_secret(mount_point=os.environ['MOUNT_POINT'], path=os.environ['SECRETS_PATH']+'/'+entry.title, secret=dict(title=entry.title, username=entry.username, password=entry.password, notes=entry.notes))
#     except Exception as error:
#         print (error.args)

for entry in fullList:
    try:
        #create_response = client.secrets.kv.v2.create_or_update_secret('user', 'sanjay.babu@gov.bc.ca/test-load3'+'/'+entry.title, secret=dict(title=entry.title, username=entry.username, password=entry.password, notes=entry.notes))
        create_response = client.secrets.kv.v2.create_or_update_secret(mount_point=ENV_MOUNT_POINT, path=ENV_SECRETS_PATH+'/'+entry.title, secret=dict(title=entry.title, username=entry.username, password=entry.password, notes=entry.notes))
   
    except Exception as error:
        print (error.args)     

#sys.stdout = old_stdout
#log_file.close()