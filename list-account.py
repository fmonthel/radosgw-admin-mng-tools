#!/usr/bin/env python
 
import json
import rgwadmin
import argparse

# Options
parser = argparse.ArgumentParser(description='List usage of account on CEPH cluster')
parser.add_argument('--accountname', help='Accountname to report (example : flatstobj01)', action='store', dest='accountname')
args = parser.parse_args()

if(args.accountname):
	accountname = args.accountname.lower()
else:
	accountname = ""

# Parameters
access_key = '****'
secret_key = '****'
rgw_server = 'srvusceph05.flox-arts.net'
 
# Object connection
radosgw = rgwadmin.RGWAdmin(access_key,secret_key,rgw_server,secure=False)
 
# Get users and print
users = radosgw.get_users()
for user in users:
	if(accountname  and accountname != user) :
		continue;
	# Get user info
	dUser = radosgw.get_user(user)
	print "#### Account : " + user + " - Name : " +  dUser["display_name"] + " ####"
	# Get user stats
	sUser = radosgw.get_usage(user, show_summary=True)
	if(sUser["summary"]):
		gb_received = float(sUser["summary"][0]["total"]["bytes_received"])/1073741824
		gb_sent = float(sUser["summary"][0]["total"]["bytes_sent"])/1073741824
		nb_ops = sUser["summary"][0]["total"]["successful_ops"]
	else :
		gb_received = 0
		gb_sent = 0
		nb_ops = 0
	kb = 0
	# Print summary
	print "Stats - Nb ops : %d - Downloaded data : %.2f GB - Uploaded data : %.2f GB" % (nb_ops, gb_sent, gb_received)
	# Get buckets of user
	buckets = radosgw.get_bucket(uid=user)
	for bucket in buckets:
		# Get bucket infos
		dBucket = radosgw.get_bucket(bucket, stats=True)
		if dBucket["bucket_quota"]["enabled"] == False :
			# Get values
			if('rgw.main' in dBucket["usage"].keys()):
				kb = kb + dBucket["usage"]["rgw.main"]["size_kb"]
				nb_object = dBucket["usage"]["rgw.main"]["num_objects"]
				size_gb = float(dBucket["usage"]["rgw.main"]["size_kb"])/1048576
			else :
				nb_object = 0
				size_gb = 0
			# Print values
			print "- Bucket : %s (quota disabled) - Nb objects : %d - GB data : %.2f" % (bucket, nb_object, size_gb)
		elif dBucket["bucket_quota"]["enabled"] == True :
			# Get values
			if('rgw.main' in dBucket["usage"].keys()):
				kb = kb + dBucket["usage"]["rgw.main"]["size_kb"]
				nb_object = dBucket["usage"]["rgw.main"]["num_objects"]
				size_gb = float(dBucket["usage"]["rgw.main"]["size_kb"])/1048576
			else :
				nb_object = 0
				size_gb = 0
			if(dBucket["bucket_quota"]["max_objects"] <= 0):
				quota_object = 0
			else :
				quota_object = dBucket["bucket_quota"]["max_objects"]
			if(dBucket["bucket_quota"]["max_size_kb"] <= 0):
				quota_gb = 0
			else :
				quota_gb = float(dBucket["bucket_quota"]["max_size_kb"])/1048576
			# Print values
			print "- Bucket : %s (quota enabled) - Nb objects : %d (quota : %d) - GB data : %.2f (quota : %.2f GB)" % (bucket, nb_object, quota_object, size_gb, quota_gb)
	print "Usage summary for account %.2fGB\n" % (float(kb)/1048576)
