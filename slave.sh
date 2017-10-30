#!/bin/bash
yum -y install http://repo.zabbix.com/zabbix/3.4/rhel/7/x86_64/zabbix-release-3.4-2.el7.noarch.rpm
yum -y install zabbix-agent
sed -i 's/Server=127.0.0.1/Server=50.50.50.49/g' /etc/zabbix/zabbix_agentd.conf
sed -i 's/ServerActive=127.0.0.1/ServerActive=50.50.50.49/g' /etc/zabbix/zabbix_agentd.conf
systemctl start zabbix-agent
