import requests
from requests.auth import HTTPBasicAuth
import json


zabbix_admin = "Admin"
zabbix_password = "zabbix"
url = 'http://50.50.50.49/api_jsonrpc.php'
auth=HTTPBasicAuth(zabbix_admin, zabbix_password)
ip = "50.50.50.50"
payload = {
    "jsonrpc" : "2.0",
    "method" : "user.login",
    "params": {
      'user': zabbix_admin,
      'password':zabbix_password,
    },
    "auth" : None,
    "id" : 0,
}
headers = {
    'content-type': 'application/json',
}



token = requests.post(url, data=json.dumps(payload), headers=headers, auth=auth).json()['result']
print 'My auth token is ' + token

payload={
    
    "jsonrpc": "2.0",
    "method": "hostgroup.get",
    "params": {
        "output": "extend",
        "filter": {
            "name": [
                "CloudHosts"
            ]
        }
    },
    "auth": token,
    "id": 1

}
hg=requests.post(url, data=json.dumps(payload), headers=headers, auth=auth).json()['result']
if not hg:
    print "This group doesnt exist! Let's create it..."
    payload={ 
    "jsonrpc": "2.0",
    "method": "hostgroup.create",
    "params": {
        "name": "CloudHosts"
    },
    "auth": token,
    "id": 1
    }   
    hg_id=requests.post(url, data=json.dumps(payload), headers=headers, auth=auth).json()['result']['groupids'][0]
    print 'Hostgroup successfully created. The id is '+hg_id
else:
    hg_id=requests.post(url, data=json.dumps(payload), headers=headers, auth=auth).json()['result'][0]['groupid']
    print "This group exists"


payload={
    "jsonrpc": "2.0",
    "method": "template.create",
    "params": {
        "host": "CloudHosts custom template",
        "groups": {
            "groupid": hg_id
        },
    },
    "auth": token,
    "id": 1
}
template_id=requests.post(url, data=json.dumps(payload), headers=headers, auth=auth).json()['result']['templateids'][0]
print "template was created! the id is "+ template_id

payload={
    "jsonrpc": "2.0",
    "method": "host.create",
    "params": {
        "host": "Hostname",
        "interfaces": [
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": 10050
            }
        ],
        "groups": [
            {
                "groupid": hg_id
            }
        ],
        "templates": [
            {
                "templateid": template_id
            }
        ],
      
    },
    "auth": token,
    "id": 1
}
host=template_id=requests.post(url, data=json.dumps(payload), headers=headers, auth=auth)
print "Success! User was created!"
