#!/usr/bin/env python
#
# create-accounts.py
#
# Simple wrapper around the Ceph radosgw account creation
#
# Author: Florent MONTHEL (fmonthel@flox-arts.net)
#

import ConfigParser
import rgwadmin
import argparse
import random
import time
import re
from datetime import datetime
from time import strftime
from terminaltables import AsciiTable

# Functions
def generate_secret() :
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    pw_length = 20
    mypw = ""
    for i in range(pw_length):
        next_index = random.randrange(len(alphabet))
        mypw = mypw + alphabet[next_index]
    return mypw

# Parameters
Config = ConfigParser.ConfigParser()
Config.read('conf/config.ini')

# Options
parser = argparse.ArgumentParser(description='Create object account on Ceph cluster for OpenStack Swift and Amazon S3')
parser.add_argument('trigram', help='Trigram of account owner (example : fla)', action='store')
parser.add_argument('email', help='Email of account owner (example : fmonthel@flox-arts.net)', action='store')
parser.add_argument('--readonly-key', help='Create readonly access key', action='store_true', dest='readkey')
parser.add_argument('--fullright-key', help='Create full right access key', action='store_true', dest='fullkey')
parser.add_argument('--secretkey', help='Secret key for access keys', action='store', default=None, dest='secretkey')

args = parser.parse_args()

# Input user secretkey
if(args.secretkey):
    secretkey = args.secretkey
else:
    secretkey = generate_secret()
 
# Other mandatory inputs
trigram = args.trigram.lower()
email = args.email.lower()

# Object connection
radosgw = rgwadmin.RGWAdmin(Config.get('RGW','rgw_access_key'),Config.get('RGW','rgw_secret_key'),Config.get('RGW','rgw_server'),secure=False,verify=False)

# Get users
dUsers = radosgw.get_users()

# Loop on users to increment id
max = 1
for user in dUsers:
    match = re.search(r"^" + trigram + Config.get('ACCOUNT','account_env') + "cos" + "([0-9]{2})$",user)
    if(match):
        if(int(match.group(1)) >= max) :
            max = int(match.group(1)) + 1
    
# Accountname generated
max = str("%02d" % max)
accountname = trigram + Config.get('ACCOUNT','account_env') + "cos" + max
displayname = (trigram + " " + Config.get('ACCOUNT','account_env') + " object account " + email).upper()


# Create RadosGW account 
if(radosgw.create_user(uid=accountname,display_name=displayname,access_key=secretkey,key_type='s3')):
    time.sleep( 5 )
    print "#### Object storage accountname created : "+accountname+" ####"
    # Delete Temporary key
    radosgw.remove_key(access_key=secretkey,key_type='s3',uid=accountname)
    # Create subuser fullright if needed
    if(args.fullkey) :
        # Create subuser FULL (usr001)
        radosgw.create_subuser(uid=accountname,subuser=accountname+'usr001',access='full')
        # Generate key for S3 (on subuser)
        radosgw.create_key(uid=accountname,subuser=accountname+'usr001',key_type='s3',access_key=accountname+'usr001',secret_key=secretkey,generate_key=None);
        print " - Full right access key created for Amazon S3 : "+accountname+"usr001 - Associated secret key : "+secretkey
        # Generate key for Swift (on subuser)
        radosgw.create_key(uid=accountname,subuser=accountname+'usr001',key_type='swift',access_key=accountname+'usr001',secret_key=secretkey,generate_key=None);
        print " - Full right access key created for OpenStack Swift : "+accountname+":"+accountname+"usr001 - Associated secret key : "+secretkey
    # Create subuser readonly if needed
    if(args.readkey) :
        # Create subuser READ (usr301)
        radosgw.create_subuser(uid=accountname,subuser=accountname+'usr301',access='read')
        # Generate key for S3 (on subuser)
        radosgw.create_key(uid=accountname,subuser=accountname+'usr301',key_type='s3',access_key=accountname+'usr301',secret_key=secretkey,generate_key=None);
        print " - Readonly access key created for Amazon S3 : "+accountname+"usr301 - Associated secret key : "+secretkey
        # Generate key for Swift (on subuser)
        radosgw.create_key(uid=accountname,subuser=accountname+'usr301',key_type='swift',access_key=accountname+'usr301',secret_key=secretkey,generate_key=None);
        print " - Readonly access key created for OpenStack Swift : "+accountname+":"+accountname+"usr301 - Associated secret key : "+secretkey

    # Now we're going to connect with account and create buckets (if keys asked)
    if(args.fullkey) :
        radosgw = rgwadmin.RGWAdmin(accountname+'usr001',secretkey,Config.get('RGW','rgw_server'),secure=False,verify=False)
    elif (args.readkey) :
        radosgw = rgwadmin.RGWAdmin(accountname+'usr301',secretkey,Config.get('RGW','rgw_server'),secure=False,verify=False)
    if(args.fullkey or args.readkey):
    	# Create 3 buckets
    	i = 1
    	while i < 4:
            bucketname = accountname+"buck"+str("%03d" % i)
            radosgw.create_bucket(bucket=bucketname)
            print "[ Bucket "+bucketname+" created and mapped on your account ]"
            i = i + 1