# A python script that utilizes hvac and pykeepass libs and vault apis to reads credentials from KeePass and push it to vault #

# Setting things up #

# Pre-requisites #

```
#WSL: Windows Subsystem for Linux
Windows Subsystem for Linux is a compatibility layer for running Linux binary executables natively on Windows 10

1. Installation: https://docs.microsoft.com/en-us/windows/wsl/install-win10
2. Follow manual installation steps 1-6
3. Choose Ubuntu 20.04 LTS on step 6
4. Install Windows Terminal
5. Run on cmd "wsl --set-default-version 2" (Set your distribution version to WSL 2)

```

# Install python, pip, dependencies and vault #

Open Windows terminal and choose Ubuntu-20.04 and run the following commands

```
1. #Update repo
sudo apt update

2. #Install python3
sudo apt install python3

3. #Install python package manager pip
sudo apt install python3-pip

4. #Install python library to read KeePass database
pip install pykeepass

5. #Install python vault api client
pip install hvac

6. #Install json processor to process json response received from vault login with oidc and obtain vault token
sudo apt install jq

7. #Install vault (https://learn.hashicorp.com/tutorials/vault/getting-started-install)
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install vault
```

# Create a file to store environment variables #

```
touch env-dev
vi env-dev
```

Add the following to the file

```
export VAULT_ADDR=https://vault-iit-dev.apps.silver.devops.gov.bc.ca/
export VAULT_TOKEN=$(vault login -method=oidc -format json | jq -r '.auth.client_token')
export KEEPASS_PATH=<path>
export KEEPASS_PWD=<pwd>
export MOUNT_POINT=<path of key value v2 secrets engine>
```

# Execution #

run the following commands in the terminal

```
#create environment variables from the contents of the file env-dev
source env-dev

#run the script
python3 py-keepass-vault.py
```
