#!/usr/bin/env python3

import xmltodict
import json
import sys 

import argparse
from pprint import pprint
from jsonpath_ng.ext import parse

def parseOptions():
    '''Parse the commandline options'''

    parser = argparse.ArgumentParser(description='''jsonpath for federation data''')
    parser.add_argument('--file', '-f', dest='infile'      ,default="small-subset.xml")
    parser.add_argument('--verbose',  '-v'  ,default=False, action="store_true"
                                            ,help='Verbosity')
    args = parser.parse_args()
    return args

def jprint(jsondata, do_print=True):
    retval = json.dumps(jsondata, sort_keys=True, indent=4, separators=(',', ': '))
    if do_print:
        print (retval)
    else:
        return retval

def jsonpath_to_list (path):
    p = str(path)
    path = p.split('.')

    for i in range(0,len( path)):
        try:
            path[i]= int( path[i].replace("]", "").replace("[", "") )
        except ValueError:
            pass
    return path

def get_from_path (jsondata, path, depth):
    def returner(data, path):
        return data[path]

    if len(path) < depth:
        depth = len(path)

    data = jsondata
    for i in range(0, depth):
        # print (F"{i}: {path[i]}")
        try:
            data = returner (data, path[i])
        except KeyError:
            # print (F"KeyError: {i}: {path[i]}")
            pass
    return data


args = parseOptions()

with open(args.infile, "r") as filehandle:
    xmldata = filehandle.read()
print ("File read")

# get rid of the unparseable colon: (or use '*' in the pathspec)
# xmldata = xmldata\
#         .replace("refeds.org/category/research-and-scholarship", "refeds-rns")

jsondata = xmltodict.parse(xmldata)
print ("conversion to json done")
# result = parse('$.*.mdxEntityDescriptor[*].mdxExtensions.mdattrxEntityAttributes[*].samlxAttribute[?samlxAttributeValue[*]="httpxrefeds-rns"]').find(jsondata)
result = parse('$.*.*[*].*.*[*].*[?*[*]="http://refeds.org/category/research-and-scholarship"]').find(jsondata)
print ("parsing done")



entityIDs=[]
for entry in result:
    path   = jsonpath_to_list(entry.full_path)
    entity = get_from_path(jsondata, path, 3)
    entityID = entity['@entityID']
    entityIDs.append(entityID)

jprint (entityIDs)

print (F"Number of Results: {len(result)}")
