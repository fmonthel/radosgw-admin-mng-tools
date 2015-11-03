#!/usr/bin/env python
#
# list-buckets.py
#
# Simple wrapper around the Ceph buckets dumps
#
# Author: Florent MONTHEL (fmonthel@flox-arts.net)
#

import rgwadmin
import argparse
from terminaltables import AsciiTable

# Parameters
access_key = 'costmpobj01'
secret_key = 'xxxxxxx'
rgw_server = 'objtmp01.flox-arts.net'
ssl = False

# Options
parser = argparse.ArgumentParser(description='List usage of buckets on Ceph cluster')
parser.add_argument('--bucketname', help='Filter on bucketname (example : flatstobj01buck001)', action='store', dest='bucketname')
parser.add_argument('--accountname', help='Filter on accountname (example : flatstobj01)', action='store', dest='accountname')

args = parser.parse_args()

if(args.bucketname):
	bucketname = args.bucketname.lower()
else:
	bucketname = ""
	
if(args.accountname):
	accountname = args.accountname.lower()
else:
	accountname = ""

# Object connection
radosgw = rgwadmin.RGWAdmin(access_key,secret_key,rgw_server,secure=ssl,verify=False)

# Get buckets impacted
if(bucketname):
	dBuckets = [bucketname, radosgw.get_bucket(bucket=bucketname, stats=True)]
elif(accountname):
	dBuckets = radosgw.get_bucket(uid=accountname, stats=True)
else:
	dBuckets = radosgw.get_bucket(stats=True)

# Get global usage to build bucket OPs
dBucketsUsage = {}
dUsage = radosgw.get_usage(show_entries=True,show_summary=True)
for dOwner in dUsage["entries"]:
	for dBucket in dOwner["buckets"]:
		dBucketsUsage[dBucket["bucket"]] = {'ok_ops':0, 'ko_ops':0, 'received_kb':0, 'sent_kb':0}
		for item in dBucket["categories"]:
			# Build bucket dic
			dBucketsUsage[dBucket["bucket"]]['ok_ops'] = dBucketsUsage[dBucket["bucket"]]['ok_ops'] + item["successful_ops"]
			dBucketsUsage[dBucket["bucket"]]['ko_ops'] = dBucketsUsage[dBucket["bucket"]]['ko_ops'] + (item["ops"] - item["successful_ops"])
			dBucketsUsage[dBucket["bucket"]]['received_kb'] = dBucketsUsage[dBucket["bucket"]]['received_kb'] + float(item["bytes_received"]/1024)
			dBucketsUsage[dBucket["bucket"]]['sent_kb'] = dBucketsUsage[dBucket["bucket"]]['sent_kb'] + float(item["bytes_sent"]/1024)

# Ascii table
myAsciiTable = [['Bucket name','Owner','Pool','Created','Obj nb','Obj quota','GB size','GB quota','OP(s) OK','OP(s) KO', 'GB upl', 'GB dl']]

# Global usage
kb_total = obj_total = kb_quota_total = obj_quota_total = ops_ko_total = ops_ok_total = kb_received_total = kb_sent_total = 0

# Loop on bucket
for dBucket in dBuckets:
	# Need to loop on good element in the list
	if(type(dBucket) is not dict):
		continue;
	# Get std info
	bucket = dBucket["bucket"]
	owner = dBucket["owner"]
	created = dBucket["mtime"]
	pool = dBucket["pool"]
	# Get values usage
	if('rgw.main' in dBucket["usage"].keys()):
		nb_object = dBucket["usage"]["rgw.main"]["num_objects"]
		size_gb = float(dBucket["usage"]["rgw.main"]["size_kb"])/1048576
		# Global value
		kb_total = kb_total + dBucket["usage"]["rgw.main"]["size_kb"]
		obj_total = obj_total + dBucket["usage"]["rgw.main"]["num_objects"]
	else:
		nb_object = size_gb = 0
	# Quota specific
	if(dBucket["bucket_quota"]["enabled"] == True):
		if(dBucket["bucket_quota"]["max_objects"] <= 0):
			quota_object = 0
		else:
			quota_object = dBucket["bucket_quota"]["max_objects"]
			obj_quota_total = obj_quota_total + dBucket["bucket_quota"]["max_objects"]
		if(bucket["bucket_quota"]["max_size_kb"] <= 0):
			quota_gb = 0
		else:
			quota_gb = float(dBucket["bucket_quota"]["max_size_kb"])/1048576
			kb_quota_total = kb_quota_total + dBucket["bucket_quota"]["max_size_kb"]
	else:
		quota_object = quota_gb = 0
	# Get stats usage
	if(bucket in dBucketsUsage.keys()):
		ops_ok = dBucketsUsage[bucket]['ok_ops']
		ops_ko = dBucketsUsage[bucket]['ko_ops']
		received_gb = float(dBucketsUsage[bucket]['received_kb'])/1048576
		sent_gb = float(dBucketsUsage[bucket]['sent_kb'])/1048576
		# Global value
		ops_ok_total = ops_ok_total + dBucketsUsage[bucket]['ok_ops']
		ops_ko_total = ops_ko_total + dBucketsUsage[bucket]['ko_ops']
		kb_received_total = kb_received_total + dBucketsUsage[bucket]['received_kb']
		kb_sent_total = kb_sent_total + dBucketsUsage[bucket]['sent_kb']
	else:
		ops_ok = ops_ko = received_gb = sent_gb = 0
	# Print values and build list
	tmpdata = list()
	tmpdata.append(bucket) # Bucketname
	tmpdata.append(owner) # Owner
	tmpdata.append(pool) # Pool on Ceph
	tmpdata.append(created) # Created date
	tmpdata.append(str(nb_object)) # Number of objets
	tmpdata.append(str(quota_object)) # Quota on objects
	tmpdata.append(str(round(size_gb,1))) # GB size
	tmpdata.append(str(round(quota_gb,1))) # Quota on size
	tmpdata.append(str(ops_ok)) # OPs OK number
	tmpdata.append(str(ops_ko)) # OPs KO number
	tmpdata.append(str(round(received_gb,1))) # GB received
	tmpdata.append(str(round(sent_gb,1))) # GB sent
	myAsciiTable.append(tmpdata)

# Get total values and print AsciiTable
tmpdata = list()
tmpdata.append("Total : " + str(len(myAsciiTable) - 1) + " bucket(s)")
tmpdata.append("")
tmpdata.append("")
tmpdata.append("")
tmpdata.append(str(obj_total))
tmpdata.append(str(obj_quota_total))
tmpdata.append(str(round(float(kb_total)/1048576,1)))
tmpdata.append(str(round(float(kb_quota_total)/1048576,1)))
tmpdata.append(str(ops_ok_total))
tmpdata.append(str(ops_ko_total))
tmpdata.append(str(round(float(kb_received_total)/1048576,1)))
tmpdata.append(str(round(float(kb_sent_total)/1048576,1)))
myAsciiTable.append(tmpdata)
# Create AsciiTable
myTable = AsciiTable(myAsciiTable)
myTable.inner_footing_row_border = True
myTable.justify_columns[4] = myTable.justify_columns[5] = myTable.justify_columns[6] = myTable.justify_columns[7] = 'right'
myTable.justify_columns[8] = myTable.justify_columns[9] = myTable.justify_columns[10] = myTable.justify_columns[11] = 'right'
# Output data
print myTable.table