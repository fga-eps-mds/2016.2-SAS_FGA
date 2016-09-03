#!/bin/bash
cd /vagrant
if [ -a /usr/local/bin/python3.5 ]
then
	mkvirtualenv -p /usr/local/bin/python3.5 sas
else
	mkvirtualenv -p /usr/local/bin/python3.4 sas
fi
workon sas
pip install -r requerements.txt
