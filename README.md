# Setting things up #

# Pre-requisites #

```
wsl/linux
```

# Install python, pip, dependencies and vault #

```
run

sudo apt update

sudo apt install python3
sudo apt install python3-pip

pip install pykeepass
pip install hvac
sudo apt install jq

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

```
source env-dev

python3 py-keepass-vault.py

```
