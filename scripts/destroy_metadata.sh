#!/bin/bash
# Note: The following command uses shell parameter expansion ```(e.g. "${path//\'/}")``` to remove single quotes from entry titles.
IFS=$'\n'
for path in $(vault kv list -format yaml user/$SECRETS_PATH | sed -re 's/^- //'); do vault kv metadata delete "user/$SECRETS_PATH/${path//\'/}"; done