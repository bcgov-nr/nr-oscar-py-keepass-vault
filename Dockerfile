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

# ENV VAULT_ADDR https://vault-iit-dev.apps.silver.devops.gov.bc.ca/
# ENV VAULT_TOKEN s.HYU1PknFsY1Gyt5ccuFPgkHC
# ENV KEEPASS_PATH sample.kdbx
# ENV KEEPASS_PWD 12345678
# ENV MOUNT_POINT user/
# ENV SECRETS_PATH sanjay.babu@gov.bc.ca/new-load/

#RUN source env-dev

#ADD test.py /home/test.py
#ADD sample.kdbx /home/sample.kdbx
#ADD py-keepass-vault.py /home/py-keepass-vault.py
#ADD env-dev /home/env-dev
WORKDIR /home

#CMD ["python3 py-keepass-vault.py"]
#ENTRYPOINT [ "/bin/bash", "-l", "-c" ]
#ENTRYPOINT [ "/bin/bash", "-l", "-c" ]
#ENTRYPOINT ["bash"]
#CMD ["py-keepass-vault.py"]
#ENTRYPOINT ["python3"]
