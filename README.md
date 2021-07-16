# Create a file to store environment variables #

Uses pykeepass and hvac libraries

```
touch env-dev
vi env-dev
```

```
export VAULT_ADDR=https://vault-iit-dev.apps.silver.devops.gov.bc.ca/
export VAULT_TOKEN=$(vault login -method=oidc -format json | jq -r '.auth.client_token')
export KEEPASS_PATH=path
export KEEPASS_PWD=pwd
export MOUNT_POINT=path of secrets engine
```

run

```
source env-dev

python3 py-keepass-vault.py

```