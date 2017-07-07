#!/usr/bin/env python
import os
import subprocess
import json
from datetime import datetime

s = subprocess.check_output(['openstack',  'server',  'list',  '-f',  'json',  '--all-project'])

dead_vm = []
dead_vm_count = 0

long_vm_list={}

ten_days = datetime.strptime("2017-06-11T01:00:00.000000", '%Y-%m-%dT%H:%M:%S.%f') - datetime.strptime("2017-06-01T01:00:00.000000", '%Y-%m-%dT%H:%M:%S.%f')

def get_vm_details(server_id):
    server_details =  subprocess.check_output(['openstack',  'server',  'show',  server_id,  '-f',  'json'])
    return json.loads(server_details)

def get_vm_uptime(server):
    vm_start = datetime.strptime(server["OS-SRV-USG:launched_at"], '%Y-%m-%dT%H:%M:%S.%f')
    current = datetime.now()
    return (current-vm_start)

def get_project_name(project_id):
    project_details = subprocess.check_output(['openstack',  'project',  'show', project_id, '-f',  'json'])
    project = json.loads(project_details)

    return project["name"]

for server in json.loads(s):
#    print server["Name"] + " " +  server["Status"]
#    {u'Status': u'ACTIVE', u'Name': u'lucius_ubuntu1604', u'Networks': u'to_ECN=10.68.32.205', u'ID': u'6d1c0ba6-b9c9-441e-8220-c64641ed9da0'}

    if server["Status"] != "ACTIVE":
        dead_vm.append(server["ID"])
        dead_vm_counter = dead_vm_counter + 1
    else:
        srv = get_vm_details(server["ID"])
        t = get_vm_uptime(srv)
        if(t > ten_days):
            #print srv

            if srv["project_id"] not in long_vm_list:
                long_vm_list[srv["project_id"]]=[]

            long_vm_list[srv["project_id"]].append({'vm_name':srv["name"], 'alive_time':str(t)})

print "----------------------------------------------------------"
#print long_vm_list

for project, vms in long_vm_list.iteritems():
    print "project name: " + get_project_name(project)
    print ".................................."
    for vm in vms:
        print vm
    print ".................................."

print "----------------------------------------------------------"
