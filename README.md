# Sistema de Alocação de Salas - SAS
O projeto tem como finalidade desenvolver um software para o gerenciamento de espaços na universidade de Brasília, especificamente a Faculdade Gama - FGA. O trabalho está sendo desenvolvido pelos alunos do curso de Engenharia de Software que frequentam as aulas de Métodos de Desenvolvimento de Software e Gestão de Portifólios e Projetos.

O status do projeto pode ser acompanhando pelos seguintes indicadores:

|Branch|Travis|Coveralls|Code Climate|
|------|------|---------|------------|
|Master|[![Build Status](https://travis-ci.org/fga-gpp-mds/2016.2-SAS_FGA.svg?branch=master)](https://travis-ci.org/fga-gpp-mds/2016.2-SAS_FGA)|[![Coverage Status](https://coveralls.io/repos/github/fga-gpp-mds/2016.2-SAS_FGA/badge.svg?branch=master)](https://coveralls.io/github/fga-gpp-mds/2016.2-SAS_FGA?branch=master)| --- |
|Dev  |[![Build Status](https://travis-ci.org/fga-gpp-mds/2016.2-SAS_FGA.svg?branch=dev)](https://travis-ci.org/fga-gpp-mds/2016.2-SAS_FGA)| [![Coverage Status](https://coveralls.io/repos/github/fga-gpp-mds/2016.2-SAS_FGA/badge.svg?branch=dev)](https://coveralls.io/github/fga-gpp-mds/2016.2-SAS_FGA?branch=dev) | [![Code Climate](https://codeclimate.com/github/fga-gpp-mds/2016.2-SAS_FGA/badges/gpa.svg)](https://codeclimate.com/github/fga-gpp-mds/2016.2-SAS_FGA) |


# Configurar o ambiente
A fim de configurar o ambiente em sua máquina pessoal, basta seguir os seguintes passos, tendo em vista o sistema operacional utilizado:

## Máquina virtual
Caso não use o Linux, em qualquer distribuição, faça uso de uma máquina virtual.

O ambiente de desenvolvimento pode ser configurado da seguinte maneira:

1. Instale o [Vagrant](https://www.vagrantup.com/)
2. Instale a máquina virtual: [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
3. Clone o projeto no diretório desejado
  - ```git clone https://github.com/fga-gpp-mds/2016.2-SAS_FGA.git```
4. Entre no projeto clonado
  - ```cd 2016.2-SAS_FGA```
5. Inicie o vagrant 
  - ```vagrant up```
6. Acesse a máquina via SSH
  - ```vagrant ssh```
7. Vá ao diretório /vagrant/
  - ```cd /vagrant/```
8. Crie um ambiente de desenvolvimento virtual
  - ```mkvirtualenv -p /urs/local/bin/python3.5 sas```
9. Finalmente, instale as dependências necessárias 
  - ```pip install -r requirements.txt```

## Linux
Caso você já utilize o Linux como sistema operacional, siga:

1. Clone o projeto
  - ```git clone https://github.com/fga-gpp-mds/2016.2-SAS_FGA.git```
2. Entre no projeto clonado
  - ```cd 2016.2-SAS_FGA```
3. Permita acesso ao arquivo de instalação
  - ```chmod 777 install-apt.sh```
4. Realize a instalação
  - ```sudo ./install-apt.sh```
5. Crie um ambiente de desenvolvimento virtual
  - ```python3 -m venv sas```
6. Iniciar o ambiente virtual
  - ```. sas/bin/activate```
7. Finalmente, instale as dependências necessárias 
  - ```pip install -r requirements.txt```

