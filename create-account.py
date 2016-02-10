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
import re
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
parser.add_argument('--readonly-key', help='Create readonly access key', action='store_true', dest='rokey')
parser.add_argument('--writeonly-key', help='Create writeonly access key', action='store_true', dest='wokey')
parser.add_argument('--readwrite-key', help='Create read/write access key', action='store_true', dest='rwkey')
parser.add_argument('--fullright-key', help='Create full right access key', action='store_true', dest='fullkey')
parser.add_argument('--buckets-nb', help='Number of bucket(s)/container(s) to create', action='store', default=3, dest='bucketsnb', type=int)


args = parser.parse_args()
 
# Mandatory inputs
trigram = args.trigram.lower()
email = args.email.lower()
bucketsnb = int(args.bucketsnb)

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
if(radosgw.create_user(uid=accountname,display_name=displayname,access_key=accountname,key_type='s3')):

    # Delete Temporary key
    radosgw.remove_key(access_key=accountname,key_type='s3',uid=accountname)
    # Ascii table
    myAsciiTableKey = [['Protocol','Permissions','Access key','Secret key']]

    # Create subuser fullright if needed
    if(args.fullkey) :
        
        # Generate subuser and secretkey
        subuser = accountname+'usr001'
        secretkey = generate_secret()
        
        # Create subuser FULL (usr001)
        radosgw.create_subuser(uid=accountname,subuser=subuser,access='full')
        
        # Generate key for S3 (on subuser)
        radosgw.create_key(uid=accountname,subuser=subuser,key_type='s3',access_key=subuser,secret_key=secretkey,generate_key=None);
		# Print values and build list for Swift
        tmpdata = list()
        tmpdata.append("S3")
        tmpdata.append("Full-control") # Permissions
        tmpdata.append(subuser) # Accesskey
        tmpdata.append(secretkey) # Secretkey
        myAsciiTableKey.append(tmpdata)
        
        # Generate key for Swift (on subuser)
        radosgw.create_key(uid=accountname,subuser=subuser,key_type='swift',access_key=subuser,secret_key=secretkey,generate_key=None);
		# Print values and build list for Swift
        tmpdata = list()
        tmpdata.append("Swift")
        tmpdata.append("Full-control") # Permissions
        tmpdata.append(accountname+":"+subuser) # Accesskey
        tmpdata.append(secretkey) # Secretkey
        myAsciiTableKey.append(tmpdata)
        
    # Create subuser read/write if needed
    if(args.rwkey) :

        # Generate subuser and secretkey
        subuser = accountname+'usr101'
        secretkey = generate_secret()
        
        # Create subuser FULL (usr001)
        radosgw.create_subuser(uid=accountname,subuser=subuser,access='readwrite')
        
        # Generate key for S3 (on subuser)
        radosgw.create_key(uid=accountname,subuser=subuser,key_type='s3',access_key=subuser,secret_key=secretkey,generate_key=None);
		# Print values and build list for Swift
        tmpdata = list()
        tmpdata.append("S3")
        tmpdata.append("Read/Write") # Permissions
        tmpdata.append(subuser) # Accesskey
        tmpdata.append(secretkey) # Secretkey
        myAsciiTableKey.append(tmpdata)
        
        # Generate key for Swift (on subuser)
        radosgw.create_key(uid=accountname,subuser=subuser,key_type='swift',access_key=subuser,secret_key=secretkey,generate_key=None);
		# Print values and build list for Swift
        tmpdata = list()
        tmpdata.append("Swift")
        tmpdata.append("Read/Write") # Permissions
        tmpdata.append(accountname+":"+subuser) # Accesskey
        tmpdata.append(secretkey) # Secretkey
        myAsciiTableKey.append(tmpdata)

    # Create subuser write-only if needed
    if(args.wokey) :

        # Generate subuser and secretkey
        subuser = accountname+'usr201'
        secretkey = generate_secret()
        
        # Create subuser FULL (usr001)
        radosgw.create_subuser(uid=accountname,subuser=subuser,access='write')
        
        # Generate key for S3 (on subuser)
        radosgw.create_key(uid=accountname,subuser=subuser,key_type='s3',access_key=subuser,secret_key=secretkey,generate_key=None);
		# Print values and build list for Swift
        tmpdata = list()
        tmpdata.append("S3")
        tmpdata.append("Write-only") # Permissions
        tmpdata.append(subuser) # Accesskey
        tmpdata.append(secretkey) # Secretkey
        myAsciiTableKey.append(tmpdata)
        
        # Generate key for Swift (on subuser)
        radosgw.create_key(uid=accountname,subuser=subuser,key_type='swift',access_key=subuser,secret_key=secretkey,generate_key=None);
		# Print values and build list for Swift
        tmpdata = list()
        tmpdata.append("Swift")
        tmpdata.append("Write-only") # Permissions
        tmpdata.append(accountname+":"+subuser) # Accesskey
        tmpdata.append(secretkey) # Secretkey
        myAsciiTableKey.append(tmpdata)
    
    # Create subuser read-only if needed
    if(args.rokey) :

        # Generate subuser and secretkey
        subuser = accountname+'usr301'
        secretkey = generate_secret()
        
        # Create subuser FULL (usr001)
        radosgw.create_subuser(uid=accountname,subuser=subuser,access='read')
        
        # Generate key for S3 (on subuser)
        radosgw.create_key(uid=accountname,subuser=subuser,key_type='s3',access_key=subuser,secret_key=secretkey,generate_key=None);
		# Print values and build list for Swift
        tmpdata = list()
        tmpdata.append("S3")
        tmpdata.append("Read-only") # Permissions
        tmpdata.append(subuser) # Accesskey
        tmpdata.append(secretkey) # Secretkey
        myAsciiTableKey.append(tmpdata)
        
        # Generate key for Swift (on subuser)
        radosgw.create_key(uid=accountname,subuser=subuser,key_type='swift',access_key=subuser,secret_key=secretkey,generate_key=None);
		# Print values and build list for Swift
        tmpdata = list()
        tmpdata.append("Swift")
        tmpdata.append("Read-only") # Permissions
        tmpdata.append(accountname+":"+subuser) # Accesskey
        tmpdata.append(secretkey) # Secretkey
        myAsciiTableKey.append(tmpdata)

    # Now we're going to connect with account and create buckets (if keys asked)
    if(subuser and secretkey) :
        radosgw_usr = rgwadmin.RGWAdmin(subuser,secretkey,Config.get('RGW','rgw_server'),secure=False,verify=False)
    	# Create buckets
    	i = 1
        buckets_list = ""
    	while i <= bucketsnb:
            bucketname = accountname+"buck"+str("%03d" % i)
            radosgw_usr.create_bucket(bucket=bucketname)
            if(i == 1):
                buckets_list = bucketname
            else:
                buckets_list = buckets_list+"\n"+bucketname
            i = i + 1
    
    # Now get info of account and print values
	dUser = radosgw.get_user(accountname)
	# Get std info
	account = accountname
	displayname = dUser["display_name"]
	max_buckets = dUser["max_buckets"]
	nb_s3keys = len(dUser["keys"])
	nb_swkeys = len(dUser["swift_keys"])
	if(dUser["suspended"]):
		suspended = "yes"
	else:
		suspended = "no"

    # Ascii table
    myAsciiTableAccount = [['Account','Display name','Suspended','S3 key(s)','Swift key(s)','Bucket(s) created','Max bucket(s)']]
	# Print values and build list
    tmpdata = list()
    tmpdata.append(account) # Accountname
    tmpdata.append(displayname) # Displayname
    tmpdata.append(suspended) # Suspended
    tmpdata.append(str(nb_s3keys)) # S3 key(s)
    tmpdata.append(str(nb_swkeys)) # Swift key(s)
    tmpdata.append(str(buckets_list)) # Bucket(s)
    tmpdata.append(str(max_buckets)) # Max buckets
    myAsciiTableAccount.append(tmpdata)
    
    # Create AsciiTable for account
    myTable = AsciiTable(myAsciiTableAccount)
    myTable.justify_columns[3] = myTable.justify_columns[4] = myTable.justify_columns[6] = 'right'
    # Output data
    print "\n#### ACCOUNT INFORMATION (JUST CREATED) ####"
    print myTable.table
    
    # Create AsciiTable for key(s)
    myTable = AsciiTable(myAsciiTableKey)
    # Output data
    print "\n#### S3/SWIFT API KEY(S) INFORMATION ####"
    print myTable.table