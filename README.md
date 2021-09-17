# A python script that utilizes hvac and pykeepass libs and vault apis to read credentials from KeePass and push it to vault #

## Setting things up ##

## 1. Pre-requisites: ##

```
#git: https://git-scm.com/downloads
#Docker: https://www.docker.com/products/docker-desktop

```
## 2. Clone the repo and copy the KeePass file into the repo

## 3. Replace the following environment variables in env-dev file with appropriate values ##

### Obtain vault token from UI by going to https://vault-iit-dev.apps.silver.devops.gov.bc.ca/ and click on profile icon on the top right hand corner and Copy token
### Sample KeePass file password: 12345678

```
VAULT_ADDR=https://vault-iit-dev.apps.silver.devops.gov.bc.ca/
VAULT_TOKEN=
KEEPASS_PATH=<keepass_file.kdbx>
KEEPASS_PWD=<pwd>
SECRETS_PATH=your_email/new_path

```

## 4. Execution ##

### Example 1: Load keepass data to a user path in the dev environment ###

Run the following commands in the terminal:

```
#build the image
docker build -t "appdev:py-keepass-vault" .

#run the script
docker run --rm --name vaultloader --env-file env-dev -v "$(pwd):/home" appdev:py-keepass-vault bash -c "python3 py-keepass-vault.py"

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
