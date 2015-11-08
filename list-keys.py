#!/usr/bin/env python
#
# list-keys.py
#
# Simple wrapper around the Ceph keys dumps
#
# Author: Florent MONTHEL (fmonthel@flox-arts.net)
#

import ConfigParser
import rgwadmin
import argparse
import time
from datetime import datetime
from time import strftime
from terminaltables import AsciiTable

# Parameters
Config = ConfigParser.ConfigParser()
Config.read('conf/config.ini')

# Options
parser = argparse.ArgumentParser(description='List keys of accounts on Ceph cluster')
parser.add_argument('--accountname', help='Filter on accountname (example : flatstobj01)', action='store', dest='accountname')
parser.add_argument('--protocol', help='Filter on S3 or Swift keys (example : S3)', action='store', dest='protocol')

args = parser.parse_args()
	
if(args.accountname):
	accountname = args.accountname.lower()
else:
	accountname = ""
if(args.protocol):
	protocol = args.protocol.lower()
else:
	protocol = ""

# Object connection
radosgw = rgwadmin.RGWAdmin(Config.get('RGW','rgw_access_key'),Config.get('RGW','rgw_secret_key'),Config.get('RGW','rgw_server'),secure=False,verify=False)

# Get users
dUsers = radosgw.get_users()

# Ascii table
myAsciiTable = [['Access key','Account','Suspended','Type','Owner (subuser or user)','Permissions']]

# Loop on users
for user in dUsers:
	# Need to loop on good element in the list
	if(accountname  and accountname != user) :
		continue
	# Get user info
	dUser = radosgw.get_user(user)
	# Get std info
	account = user
	if(dUser["suspended"]):
		suspended = "yes"
	else:
		suspended = "no"
	# Loop on subusers first and build dic
	dSubusers = {}
	for subuser in dUser['subusers']:
		dSubusers[ subuser['id'] ] = {'permissions':subuser['permissions']}
	# Loop now on S3 keys
	if(protocol == ''or protocol == "s3"):
		for keys in dUser['keys']:
			# Get infos
			access_key = keys['access_key']
			owner = keys['user']
			if(owner in dSubusers.keys()):
				permissions = dSubusers[ owner ]['permissions']
			else:
				permissions = 'full-control'
			# Print values and build list
			tmpdata = list()
			tmpdata.append(access_key) # Accesskey
			tmpdata.append(account) # Account
			tmpdata.append(suspended) # Suspended
			tmpdata.append("S3")
			tmpdata.append(owner) # Owner
			tmpdata.append(permissions) # Permissions
			myAsciiTable.append(tmpdata)
	# Loop now on Swift keys
	if(protocol == ''or protocol == "swift"):
		for keys in dUser['swift_keys']:
			# Get infos
			access_key = keys['user']
			owner = keys['user']
			if(owner in dSubusers.keys()):
				permissions = dSubusers[ owner ]['permissions']
			else:
				permissions = 'full-control'
			# Print values and build list
			tmpdata = list()
			tmpdata.append(access_key) # Accesskey
			tmpdata.append(account) # Account
			tmpdata.append(suspended) # Suspended
			tmpdata.append("Swift")
			tmpdata.append(owner) # Owner
			tmpdata.append(permissions) # Permissions
			myAsciiTable.append(tmpdata)

# Get total values and print AsciiTable
tmpdata = list()
tmpdata.append("Total : " + str(len(myAsciiTable) - 1) + " key(s)")
myAsciiTable.append(tmpdata)
# Create AsciiTable
myTable = AsciiTable(myAsciiTable)
myTable.inner_footing_row_border = True
# Output data
print myTable.table
