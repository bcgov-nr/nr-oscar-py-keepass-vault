# A python script that utilizes hvac and pykeepass libs and vault apis to reads credentials from KeePass and push it to vault #

# Setting things up #

# Pre-requisites #

```
wsl/linux
```

# Install python, pip, dependencies and vault #

run the following commands in the terminal

```
#update repo
sudo apt update

#install python3
sudo apt install python3

#install python package manager pip
sudo apt install python3-pip

#install python library to read KeePass database
pip install pykeepass

#install python vault api client
pip install hvac

#install json processor to process json response received from vault login with oidc and obtain vault token
sudo apt install jq

#install vault 
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install vault
```

# Create a file to store environment variables #

```
touch env-dev
vi env-dev
Add the following to the file
```

```
export VAULT_ADDR=https://vault-iit-dev.apps.silver.devops.gov.bc.ca/
export VAULT_TOKEN=$(vault login -method=oidc -format json | jq -r '.auth.client_token')
export KEEPASS_PATH=path
export KEEPASS_PWD=pwd
export MOUNT_POINT=path of key value v2 secrets engine
```

# Execution #

run the following commands in the terminal

```
source env-dev
python3 py-keepass-vault.py
```
