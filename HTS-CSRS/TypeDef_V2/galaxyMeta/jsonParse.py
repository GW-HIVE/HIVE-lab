#!/usr/bin/env python

import json
import pprint 
galaxy = 'Galaxy-Workflow-Metagenomics_Pipeline.json'
with open(galaxy, 'rU') as file:
    data = json.load(file)
tool = {}
for i in range(len(data['steps'].keys())):
    tool[i] = {}
    
    print data['steps'][str(i)]['id']
    tool[i]['step_number'] = data['steps'][str(i)]['id']
    print data['steps'][str(i)]['name']
    tool[i]['name'] = data['steps'][str(i)]['name']
    print data['steps'][str(i)]['tool_version']
    tool[i]['tool_version'] = data['steps'][str(i)]['tool_version']
    print data['steps'][str(i)]['tool_id']
    tool[i]['tool_id'] = data['steps'][str(i)]['tool_id']
    tool[i]['input_uri_list'] = {}
    for n in data['steps'][str(i)]['inputs']:
        print n['name'], n['description']
        tool[i]['input_uri_list']['name'] = n['name']
        tool[i]['input_uri_list']['URI'] = n['description']
    print ''
    tool[i]['output_uri_list'] = {}
    for n in data['steps'][str(i)]['outputs']:
        print n['name'], n['type']
        tool[i]['output_uri_list']['address'] = str(n['name']+'.'+n['type'])
    print '\n'
json_data = json.dumps(tool)

print(json_data)