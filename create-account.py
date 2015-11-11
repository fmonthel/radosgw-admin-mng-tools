#!/usr/bin/env python

import ConfigParser
import argparse
import re
import json
import random
import rgwadmin
import logging

# Parameters
Config = ConfigParser.ConfigParser()
Config.read('conf/config.ini')

# Options
parser = argparse.ArgumentParser(description='Create object account on CEPH cluster for OpenStack Swift and Amazon S3')
parser.add_argument('trigram', help='Trigram of account owner (example : fla)', action='store')
parser.add_argument('ownername', help='First letter of firstname and Name of account owner (example : fmonthel)', action='store')
parser.add_argument('--admin', help='Admin account to administrate cluster', action='store_true', dest='admin')
parser.add_argument('--readonly', help='Create readonly access key', action='store_true', dest='readonly')
parser.add_argument('--fullright', help='Create full right access key', action='store_true', dest='fullright')
parser.add_argument('--secretkey', help='Secret key for access keys', action='store', default=None, dest='secretkey')
args = parser.parse_args()
 
# Functions
def generate_secret() :
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    pw_length = 15
    mypw = ""
    for i in range(pw_length):
        next_index = random.randrange(len(alphabet))
        mypw = mypw + alphabet[next_index]
    return mypw
 
# Input user admin
if(args.admin):
    kind = 'adm'
else :
    kind = 'obj'
 
# Input user secretkey
if(args.secretkey):
    secretkey = args.secretkey
else:
    secretkey = generate_secret()
 
# Other mandatory inputs
trigram = args.trigram.lower()
ownername = args.ownername.lower()
 
# Object connection ADMIN
radosgw = rgwadmin.RGWAdmin(Config.get('RGW','rgw_access_key'),Config.get('RGW','rgw_secret_key'),Config.get('RGW','rgw_server'),secure=False,verify=False)
 
# Parse users and get accountname
max = 1
users = radosgw.get_users()
for user in users:
    match = re.search(r"^" + trigram + Config.get('ACCOUNT','account_env') + kind + "([0-9]{2})$",user)
    if(match):
        if(int(match.group(1)) >= max) :
            max = int(match.group(1)) + 1
    
# Accountname generated
max = str("%02d" % max)
accountname = trigram + Config.get('ACCOUNT','account_env') + kind + "" + max
if(kind == 'adm'):
    displayname = (trigram + " " + Config.get('ACCOUNT','account_env') + " adm object account " + ownername).upper()
else:
    displayname = (trigram + " " + Config.get('ACCOUNT','account_env') + " object account " + ownername).upper()
 
if(radosgw.create_user(uid=accountname,display_name=displayname,access_key=secretkey,key_type='s3')):
    print "#### Object storage accountname created : "+accountname+" ####"
    # Delete Temporary key
    radosgw.remove_key(access_key=secretkey,key_type='s3',uid=accountname)
    # Create subuser fullright if needed
    if(args.fullright) :
        radosgw.create_subuser(uid=accountname,subuser=accountname+'usr001',key_type='s3',access='full')
        user =  radosgw.get_user(accountname)
        radosgw.remove_key(access_key=user['keys'][0]['access_key'],key_type='s3',uid=accountname,subuser=accountname+'usr001')
    # Create subuser readonly if needed
    if(args.readonly) :
        radosgw.create_subuser(uid=accountname,subuser=accountname+'usr301',key_type='s3',access='read')
        user =  radosgw.get_user(accountname)
        radosgw.remove_key(access_key=user['keys'][0]['access_key'],key_type='s3',uid=accountname,subuser=accountname+'usr301')
    # Generate keys
    if(args.fullright) :
        radosgw.create_key(uid=accountname,subuser=accountname+'usr001',key_type='s3',access_key=accountname+'usr001',secret_key=secretkey,generate_key=None);
        print " - Full right access key created for Amazon S3 : "+accountname+"usr001 - Associated secret key : "+secretkey
        radosgw.create_key(uid=accountname,subuser=accountname+'usr001',key_type='swift',access_key=accountname+'usr001',secret_key=secretkey,generate_key=None);
        print " - Full right access key created for OpenStack Swift : "+accountname+":"+accountname+"usr001 - Associated secret key : "+secretkey
    if(args.readonly) :
        radosgw.create_key(uid=accountname,subuser=accountname+'usr301',key_type='s3',access_key=accountname+'usr301',secret_key=secretkey,generate_key=None);
        print " - Readonly access key created for Amazon S3 : "+accountname+"usr301 - Associated secret key : "+secretkey 
        radosgw.create_key(uid=accountname,subuser=accountname+'usr301',key_type='swift',access_key=accountname+'usr301',secret_key=secretkey,generate_key=None);
        print " - Readonly access key created for OpenStack Swift : "+accountname+":"+accountname+"usr001 - Associated secret key : "+secretkey
    # Now we're going to connect with account and create buckets (if keys asked)
    if(args.fullright) :
        radosgw = rgwadmin.RGWAdmin(accountname+'usr001',secretkey,Config.get('RGW','rgw_server'),secure=False)
    elif (args.readonly) :
        radosgw = rgwadmin.RGWAdmin(accountname+'usr301',secretkey,Config.get('RGW','rgw_server'),secure=False)
    if(args.fullright or args.readonly):
    	# Create 3 buckets
    	i = 1
    	while i < 4:
	    bucketname = accountname+"buck00"+str(i)
    	    radosgw.create_bucket(bucket=bucketname)
    	    print "[ Bucket "+bucketname+" created and mapped on your account ]"
    	    i = i + 1
