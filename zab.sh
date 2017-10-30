#!/bin/bash

yum -y install mariadb mariadb-server 

/usr/bin/mysql_install_db --user=mysql

systemctl start mariadb

mysql -uroot -e "create database zabbix character set utf8 collate utf8_bin;"
mysql -uroot -e "grant all privileges on zabbix.* to zabbix@localhost identified by 'zabbix';"

yum -y install http://repo.zabbix.com/zabbix/3.4/rhel/7/x86_64/zabbix-release-3.4-2.el7.noarch.rpm

yum -y install zabbix-server-mysql zabbix-web-mysql


zcat /usr/share/doc/zabbix-server-mysql-*/create.sql.gz | mysql -uzabbix -pzabbix zabbix

sed -i 's/# DBPassword=/DBPassword=zabbix/g' /etc/zabbix/zabbix_server.conf 
systemctl start zabbix-server 

yum -y install zabbix-web-mysql 
sed -ir 's!# php_value date.timezone Europe/Riga!php_value date.timezone Europe/Minsk!' /etc/httpd/conf.d/zabbix.conf
cat /vagrant/zabbix.conf.php >> /etc/zabbix/web/zabbix.conf.php
sed -i 's!Alias /zabbix /usr/share/zabbix!Alias / /usr/share/zabbix/!' /etc/httpd/conf.d/zabbix.conf
systemctl start httpd  
yum -y install zabbix-agent
systemctl start zabbix-agent
yum -y install python-pip
pip install requests
python /vagrant/addhost.py
