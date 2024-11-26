FROM python:3.14-rc-bookworm

RUN apt-get update && \
apt-get install -y jq && \
apt-get install -y wget && \
apt-get install -y unzip

RUN pip3 install pykeepass && \
pip3 install hvac && \
wget -O vault.zip https://releases.hashicorp.com/vault/1.18.1/vault_1.18.1_linux_amd64.zip && \
unzip vault.zip -d /usr/bin/

WORKDIR /home