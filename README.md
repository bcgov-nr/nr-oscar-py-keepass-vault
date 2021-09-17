# A python script that utilizes hvac and pykeepass libs and vault apis to read credentials from KeePass and push it to vault #

## Setting things up ##

## 1. Pre-requisites: ##


To clone the repo:  
* git: https://git-scm.com/downloads  

To build and run the image:  
* Docker (https://www.docker.com/products/docker-desktop) or Podman (https://podman.io/)  
## 2. Clone the repo and copy the KeePass file into the repo

## 3. Replace the following variables in the environment configuration file (e.g. conf/vault-test) with appropriate values ##

### Obtain vault token from UI by going to https://vault-iit-dev.apps.silver.devops.gov.bc.ca/ and click on profile icon on the top right hand corner and Copy token
### Sample KeePass file password: 12345678

```
VAULT_ADDR=https://vault-iit-test.apps.silver.devops.gov.bc.ca/
VAULT_TOKEN=<<your_token>>
KEEPASS_PATH=sample.kdbx
MOUNT_POINT=user
SECRETS_PATH=email/target_path
KEEPASS_PWD=<<keepass_password>>

```

## 4. Execution ##

### Example 1: Load keepass data to a user path in the dev environment ###

Run the following commands in the terminal:

```
#build the image
docker build -t "appdev:py-keepass-vault" .

#set environment config
export VAULT_ENV=conf/env-test

#run the script to load keepass data
podman run --rm --name vaultloader --env-file $VAULT_ENV -v "$(pwd):/home" appdev:py-keepass-vault ./scripts/load_keepass.sh

#list the data you loaded
podman run --rm --name vaultloader --env-file $VAULT_ENV -v "$(pwd):/home" appdev:py-keepass-vault ./scripts/list_secrets.sh

```

## 5. Cleanup ##

You may want to clean up after a test load. Do the following to permanently delete your test data.

Destroy secrets:
```
podman run --rm --name vaultloader --env-file $VAULT_ENV -v "$(pwd):/home" appdev:py-keepass-vault ./scripts/destroy_secrets.sh
```

Destroy metadata:
```
podman run --rm --name vaultloader --env-file $VAULT_ENV -v "$(pwd):/home" appdev:py-keepass-vault ./scripts/destroy_metadata.sh
```

## References ##

https://askubuntu.com/questions/344407/how-to-read-complete-line-in-for-loop-with-spaces  
