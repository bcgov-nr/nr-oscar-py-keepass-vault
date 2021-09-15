FROM ubuntu:latest

RUN apt update && \
apt install -y python3 && \
apt install -y python3-pip && \
apt install -y jq && \
apt install -y wget && \
apt install -y unzip 

RUN pip install pykeepass && \
pip install hvac && \
wget -O vault.zip https://releases.hashicorp.com/vault/1.8.2/vault_1.8.2_linux_amd64.zip && \
unzip vault.zip -d /usr/bin/

WORKDIR /home