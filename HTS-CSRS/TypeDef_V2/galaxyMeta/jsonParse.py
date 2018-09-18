#!/usr/bin/env python

import json
import pprint 
galaxy = 'Galaxy-Workflow-Metagenomics_Pipeline.json'
with open(galaxy, 'rU') as file:
    data = json.load(file)
tool = {}
for i in range(len(data['steps'].keys())):
#for i in data['steps'].keys()[9]:
    tool[i] = {}
    
    print data['steps'][str(i)]['id']
    tool[i]['step_number'] = data['steps'][str(i)]['id']
    print data['steps'][str(i)]['name']
    tool[i]['name'] = data['steps'][str(i)]['name']
    print data['steps'][str(i)]['tool_version']
    tool[i]['tool_version'] = data['steps'][str(i)]['tool_version']
    print data['steps'][str(i)]['tool_id']
    tool[i]['tool_id'] = data['steps'][str(i)]['tool_id']
    tool[i]['input_list'] = []
    for step in data['steps'][str(i)]['inputs']:
        print step['name'], step['description']
        a = {'name': step['name'], 'description': step['description']}
        tool[i]['input_list'].append(a)
        # tool[i]['input_list']['name']: step['name']
        # tool[i]['input_list']['URI'] = step['description']
    print ''
    tool[i]['output_list'] = []
    for step in data['steps'][str(i)]['outputs']:
        print step['name'], step['type']
        a = {'name': str(step['name']+'.'+step['type']), 'type': step['type']}
#        tool[i]['output_list']['address'] = 
        tool[i]['output_list'].append(a)
    print '\n'
json_data = json.dumps(tool)

#print(json_data)
for i in tool: 
    print json.dumps(tool[i])