# A python script that utilizes hvac and pykeepass libs and vault apis to read credentials from KeePass and push it to vault #

## Setting things up ##

## 1. Pre-requisites: ##

```
#WSL: Windows Subsystem for Linux
Windows Subsystem for Linux is a compatibility layer for running Linux binary executables natively on Windows 10

1. Installation: https://docs.microsoft.com/en-us/windows/wsl/install-win10
2. Follow manual installation steps 1-6
3. Choose Ubuntu 20.04 LTS on step 6
4. Install Windows Terminal
5. Run on cmd "wsl --set-default-version 2" (Set your distribution version to WSL 2)

```

## 2. Install python, pip, dependencies and vault ##

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

## 3. Replace environment variables in env-dev with appropriate values ##


```
export VAULT_ADDR=https://vault-iit-dev.apps.silver.devops.gov.bc.ca/
export VAULT_TOKEN=$(vault login -method=oidc -format json | jq -r '.auth.client_token')
export KEEPASS_PATH=<path>
export KEEPASS_PWD=<pwd>
export MOUNT_POINT=<path of key value v2 secrets engine>
export SECRETS_PATH=<path to secrets>
```

## 4. Execution ##

### Example 1: Load keepass data to a user path in the dev environment ###

Run the following commands in the terminal:

```
#create environment variables from the contents of the file env-dev
source env-dev

#run the script
python3 py-keepass-vault.py

#list the data you loaded
vault kv list -format yaml user/andreas.wilson@gov.bc.ca/test-load

```

## 5. Cleanup ##

You may want to clean up after a test load. Do the following to permanently delete your test data.

Note: The sample keepass file has entries with spaces. If your test entries have spaces, set IFS to newline:

```
IFS=$'\n'
```

Note: The following commands use shell parameter expansion ```(e.g. "${path//\'/}")``` to remove single quotes from entry titles.

Delete secrets:
```
for path in $(vault kv list -format yaml user/andreas.wilson@gov.bc.ca/test-load | sed -re 's/^- //'); do vault kv delete -versions=1 "user/andreas.wilson@gov.bc.ca/test-load/${path//\'/}"; done
```

Destroy secrets:
```
for path in $(vault kv list -format yaml user/andreas.wilson@gov.bc.ca/test-load | sed -re 's/^- //'); do vault kv destroy -versions=1 "user/andreas.wilson@gov.bc.ca/test-load/${path//\'/}"; done
```

Destroy metadata:
```
for path in $(vault kv list -format yaml user/andreas.wilson@gov.bc.ca/test-load | sed -re 's/^- //'); do vault kv metadata delete "user/andreas.wilson@gov.bc.ca/test-load/${path//\'/}"; done
```

If you previously set IFS to newline, unset it when finished:
```
unset IFS
```
## References ##

https://askubuntu.com/questions/344407/how-to-read-complete-line-in-for-loop-with-spaces  
