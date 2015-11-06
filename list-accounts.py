#!/usr/bin/env python
#
# list-accounts.py
#
# Simple wrapper around the Ceph buckets dumps
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
parser = argparse.ArgumentParser(description='List usage of accounts on Ceph cluster')
parser.add_argument('--accountname', help='Filter on accountname (example : flatstobj01)', action='store', dest='accountname')

args = parser.parse_args()
	
if(args.accountname):
	accountname = args.accountname.lower()
else:
	accountname = ""

# Object connection
radosgw = rgwadmin.RGWAdmin(Config.get('RGW','rgw_access_key'),Config.get('RGW','rgw_secret_key'),Config.get('RGW','rgw_server'),secure=False,verify=False)

# Get users
dUsers = radosgw.get_users()

# Get global usage to build bucket OPs
dBucketsUsage = {}
oldestUsage = time.time() # Current timestamp
newestUsage = 0 # Old timestamp :)
dUsage = radosgw.get_usage(show_entries=True,show_summary=True)
for dOwner in dUsage["entries"]:
	for dBucket in dOwner["buckets"]:
		dBucketsUsage[dBucket["bucket"]] = {'ok_ops':0, 'ko_ops':0, 'received_kb':0, 'sent_kb':0}
		if(dBucket["epoch"] < oldestUsage):
			oldestUsage = dBucket["epoch"]
		if(dBucket["epoch"] > newestUsage):
			newestUsage = dBucket["epoch"]
		for item in dBucket["categories"]:
			# Build bucket dic
			dBucketsUsage[dBucket["bucket"]]['ok_ops'] = dBucketsUsage[dBucket["bucket"]]['ok_ops'] + item["successful_ops"]
			dBucketsUsage[dBucket["bucket"]]['ko_ops'] = dBucketsUsage[dBucket["bucket"]]['ko_ops'] + (item["ops"] - item["successful_ops"])
			dBucketsUsage[dBucket["bucket"]]['received_kb'] = dBucketsUsage[dBucket["bucket"]]['received_kb'] + float(item["bytes_received"]/1024)
			dBucketsUsage[dBucket["bucket"]]['sent_kb'] = dBucketsUsage[dBucket["bucket"]]['sent_kb'] + float(item["bytes_sent"]/1024)

# Ascii table
myAsciiTable = [['Account name','Display name','Suspended','Bucket(s) nb','Max bucket(s)','Obj nb','GB size','OP(s) OK (*)','OP(s) KO (*)', 'GB upl (*)', 'GB dl (*)']]

# Global usage
kb_total = obj_total = bucket_total = max_buckets_total = ops_ko_total = ops_ok_total = kb_received_total = kb_sent_total = 0

# Loop on users
for user in dUsers:
	# Need to loop on good element in the list
	if(accountname  and accountname != user) :
		continue
	# Get user info
	dUser = radosgw.get_user(user)
	# Get std info
	account = user
	displayname = dUser["display_name"]
	max_buckets = dUser["max_buckets"]
	if(dUser["suspended"]):
		suspended = "yes"
	else:
		suspended = "no"
	# Global value
	max_buckets_total = max_buckets_total + dUser["max_buckets"]
	# Get stats usage
	sUser = radosgw.get_usage(user, show_summary=True)
	if(sUser["summary"]):
		ops_ok = sUser["summary"][0]["total"]["successful_ops"]
		ops_ko = sUser["summary"][0]["total"]["ops"] - sUser["summary"][0]["total"]["successful_ops"]
		received_gb = float(sUser["summary"][0]["total"]["bytes_received"])/1073741824
		sent_gb = float(sUser["summary"][0]["total"]["bytes_sent"])/1073741824
		# Global value
		ops_ok_total = ops_ok_total + ops_ok
		ops_ko_total = ops_ko_total + ops_ko
		kb_received_total = kb_received_total + float(sUser["summary"][0]["total"]["bytes_received"])/1024
		kb_sent_total = kb_sent_total + float(sUser["summary"][0]["total"]["bytes_sent"])/1024
	else:
		ops_ok = ops_ko = received_gb = sent_gb = 0
	# Get buckets stats of user
	dBuckets = radosgw.get_bucket(uid=user, stats=True)
	nb_bucket = len(dBuckets)
	nb_object = size_kb = 0
	# Loop on bucket
	for dBucket in dBuckets:
		# Need to loop on good element in the list
		if(type(dBucket) is not dict):
			continue;
		# Get values usage
		if('rgw.main' in dBucket["usage"].keys()):
			nb_object = nb_object + dBucket["usage"]["rgw.main"]["num_objects"]
			size_kb = size_kb + dBucket["usage"]["rgw.main"]["size_kb"]
	# GB size
	size_gb = float(size_kb)/1048576
	# Global value
	kb_total = kb_total + size_kb
	obj_total = obj_total + nb_object
	bucket_total = bucket_total + nb_bucket
	# Print values and build list
	tmpdata = list()
	tmpdata.append(account) # Accountname
	tmpdata.append(displayname) # Displayname
	tmpdata.append(suspended) # Suspended
	tmpdata.append(str(nb_bucket)) # Bucket(s) nb
	tmpdata.append(str(max_buckets)) # Max buckets
	tmpdata.append(str(nb_object)) # Number of objets
	tmpdata.append(str(round(size_gb,1))) # GB size
	tmpdata.append(str(ops_ok)) # OPs OK number
	tmpdata.append(str(ops_ko)) # OPs KO number
	tmpdata.append(str(round(received_gb,1))) # GB received
	tmpdata.append(str(round(sent_gb,1))) # GB sent
	myAsciiTable.append(tmpdata)

# Get total values and print AsciiTable
tmpdata = list()
tmpdata.append("Total : " + str(len(myAsciiTable) - 1) + " account(s)")
tmpdata.append("")
tmpdata.append("")
tmpdata.append(str(bucket_total))
tmpdata.append(str(max_buckets_total))
tmpdata.append(str(obj_total))
tmpdata.append(str(round(float(kb_total)/1048576,1)))
tmpdata.append(str(ops_ok_total))
tmpdata.append(str(ops_ko_total))
tmpdata.append(str(round(float(kb_received_total)/1048576,1)))
tmpdata.append(str(round(float(kb_sent_total)/1048576,1)))
myAsciiTable.append(tmpdata)	
# Create AsciiTable
myTable = AsciiTable(myAsciiTable)
myTable.inner_footing_row_border = True
myTable.justify_columns[3] = myTable.justify_columns[4] = myTable.justify_columns[5] = myTable.justify_columns[6] = 'right'
myTable.justify_columns[7] = myTable.justify_columns[8] = myTable.justify_columns[9] = myTable.justify_columns[10] = 'right'
# Output data
print myTable.table
print "* Stats from " + str(datetime.utcfromtimestamp(oldestUsage)) + " to " + str(datetime.utcfromtimestamp(newestUsage))