#!/bin/bash
apt-get update
apt-get install -y python3-pip
apt-get install -y vim
apt-get install -y python-virtualenv
apt-get install -y virtualenvwrapper
apt-get install -y libssl-dev openssl
wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz 
tar -xvzf Python-3.5.2.tgz
cd Python-3.5.2/
./configure --with-ensurepip=install
make
sudo make install

