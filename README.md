# Radosgw admin MNG Tools

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/1152c37781184c2c9cdfbfc6cd0f1b07)](https://www.codacy.com/app/fmonthel/radosgw-admin-mng-tools?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=fmonthel/radosgw-admin-mng-tools&amp;utm_campaign=Badge_Grade)

Scripts to manage accounts, buckets, reporting for Ceph object mode (Swift and S3)

    pip install terminaltables rgwadmin argparse

We're using radosgw-admin module (github)

##### Create account and keys :

    ./create-account.py -h
	usage: create-account.py [-h] [--readonly-key] [--writeonly-key]
	                         [--readwrite-key] [--fullright-key]
	                         [--buckets-nb BUCKETSNB]
	                         trigram email

To create account on Ceph cluster with several keys and 5 buckets/containers :

    ./create-account.py --readonly-key --writeonly-key --readwrite-key --fullright-key --buckets-nb=5 fla fmonthel@flox-arts.net
    
    #### ACCOUNT INFORMATION (JUST CREATED) ####
    +-------------+-----------------------------------------------+-----------+-----------+--------------+--------------------+---------------+
    | Account     | Display name                                  | Suspended | S3 key(s) | Swift key(s) | Bucket(s) created  | Max bucket(s) |
    +-------------+-----------------------------------------------+-----------+-----------+--------------+--------------------+---------------+
    | flatmpcos51 | FLA TMP OBJECT ACCOUNT FMONTHEL@FLOX-ARTS.NET | no        |         4 |            4 | flatmpcos51buck001 |          1000 |
    |             |                                               |           |           |              | flatmpcos51buck002 |               |
    |             |                                               |           |           |              | flatmpcos51buck003 |               |
    |             |                                               |           |           |              | flatmpcos51buck004 |               |
    |             |                                               |           |           |              | flatmpcos51buck005 |               |
    +-------------+-----------------------------------------------+-----------+-----------+--------------+--------------------+---------------+
    
    #### S3/SWIFT API KEY(S) INFORMATION ####
    +----------+--------------+-------------------------------+----------------------+
    | Protocol | Permissions  | Access key                    | Secret key           |
    +----------+--------------+-------------------------------+----------------------+
    | S3       | Full-control | flatmpcos51usr001             | aaaaaaaaabbbbbbbbbcc |
    | Swift    | Full-control | flatmpcos51:flatmpcos51usr001 | aaaaaaaaabbbbbbbbbcc |
    | S3       | Read/Write   | flatmpcos51usr101             | aaaaaaaaabbbbbbbbbcc |
    | Swift    | Read/Write   | flatmpcos51:flatmpcos51usr101 | aaaaaaaaabbbbbbbbbcc |
    | S3       | Write-only   | flatmpcos51usr201             | aaaaaaaaabbbbbbbbbcc |
    | Swift    | Write-only   | flatmpcos51:flatmpcos51usr201 | aaaaaaaaabbbbbbbbbcc |
    | S3       | Read-only    | flatmpcos51usr301             | aaaaaaaaabbbbbbbbbcc |
    | Swift    | Read-only    | flatmpcos51:flatmpcos51usr301 | aaaaaaaaabbbbbbbbbcc |
    +----------+--------------+-------------------------------+----------------------+

#####  Information on accounts :

    ./list-accounts.py -h
	usage: list-accounts.py [-h] [--accountname ACCOUNTNAME]
    
	List usage of accounts on Ceph cluster
    
	optional arguments:
	  -h, --help            show this help message and exit
	  --accountname ACCOUNTNAME
	                        Filter on accountname (example : flatstobj01)

To list all accounts on Ceph cluster :

	./list-accounts.py 
	+----------------------+----------------------------------+-----------+-----------+--------------+-----------+---------------+-----+---------+-----------+-----------+-----------+----------+
	| Account name         | Display name                     | Suspended | S3 key(s) | Swift key(s) | Bucket(s) | Max bucket(s) | Obj | GB size | OPs OK(*) | OPs KO(*) | GB upl(*) | GB dl(*) |
	+----------------------+----------------------------------+-----------+-----------+--------------+-----------+---------------+-----+---------+-----------+-----------+-----------+----------+
	| jmktmpobj01          | JMK TMP OBJECT ACCOUNT JOJOJOJOJ | no        |         2 |            2 |         3 |          1000 |  96 |     4.9 |         0 |         0 | 0.0       | 0.0      |
	| flatmpobj01          | FLA TMP OBJECT ACCOUNT FMONTHEL  | yes       |         2 |            2 |         2 |          1000 | 688 |     3.2 |        86 |        15 | 0.8       | 0.0      |
	| costmpobj01          | COS ADMIN account                | no        |         1 |            0 |         0 |          1000 |   0 |     0.0 |         0 |         0 | 0.0       | 0.0      |
	+----------------------+----------------------------------+-----------+-----------+--------------+-----------+---------------+-----+---------+-----------+-----------+-----------+----------+
	| Total : 3 account(s) |                                  |           |         5 |            4 |         5 |          3000 | 784 |     8.1 |        86 |        15 | 0.8       | 0.0      |
	+----------------------+----------------------------------+-----------+-----------+--------------+-----------+---------------+-----+---------+-----------+-----------+-----------+----------+
	* Stats from 2015-11-05 02:00:00 to 2015-11-05 23:00:00

##### Information on buckets :
 
    ./list-buckets.py -h
    usage: list-buckets.py [-h] [--bucketname BUCKETNAME]
                         [--accountname ACCOUNTNAME]
    
    List usage of buckets on Ceph cluster
     
    optional arguments:
    -h, --help            show this help message and exit
    --bucketname BUCKETNAME
                          Filter on bucketname (example : flatstobj01buck001)
    --accountname ACCOUNTNAME
                          Filter on accountname (example : flatstobj01)

To list all buckets on Ceph cluster :
 
	./list-buckets.py 
	+---------------------+-------------+--------------+---------------------+--------+-----------+---------+----------+--------------+--------------+------------+-----------+
	| Bucket name         | Owner       | Pool         | Created             | Obj nb | Obj quota | GB size | GB quota | OP(s) OK (*) | OP(s) KO (*) | GB upl (*) | GB dl (*) |
	+---------------------+-------------+--------------+---------------------+--------+-----------+---------+----------+--------------+--------------+------------+-----------+
	| jmktmpobj01buck003  | jmktmpobj01 | .rgw.buckets | 2015-10-29 05:19:25 |      0 |         0 |     0.0 |      0.0 |            1 |            0 |        0.0 |       0.0 |
	| jmktmpobj01buck001  | jmktmpobj01 | .rgw.buckets | 2015-10-29 05:19:24 |     96 |         0 |     4.9 |      0.0 |          520 |            1 |        4.8 |       0.0 |
	| flatmpobj01buck002  | flatmpobj01 | .rgw.buckets | 2015-11-01 22:57:51 |      3 |         0 |     1.9 |      0.0 |          252 |            0 |        1.9 |       1.9 |
	| jmktmpobj01buck002  | jmktmpobj01 | .rgw.buckets | 2015-10-29 05:19:25 |      0 |         0 |     0.0 |      0.0 |            1 |            0 |        0.0 |       0.0 |
	| flatmpobj01buck001  | flatmpobj01 | .rgw.buckets | 2015-10-29 05:13:27 |    684 |         0 |     0.3 |      0.0 |          722 |            0 |        0.3 |       0.0 |
	+---------------------+-------------+--------------+---------------------+--------+-----------+---------+----------+--------------+--------------+------------+-----------+
	| Total : 5 bucket(s) |             |              |                     |    783 |         0 |     7.1 |      0.0 |         1496 |            1 |        7.1 |       1.9 |
	+---------------------+-------------+--------------+---------------------+--------+-----------+---------+----------+--------------+--------------+------------+-----------+
	* Stats from 2015-10-28 04:00:00 to 2015-11-04 20:00:00

##### Information on keys :
 
	./list-keys.py -h
	usage: list-keys.py [-h] [--accountname ACCOUNTNAME] [--protocol PROTOCOL]
    
	List keys of accounts on Ceph cluster
    
	optional arguments:
	  -h, --help            show this help message and exit
	  --accountname ACCOUNTNAME
	                        Filter on accountname (example : flatstobj01)
	  --protocol PROTOCOL   Filter on S3 or Swift keys (example : S3)

To list all keys on Ceph cluster :
 
	./list-keys.py
	+-------------------------------+-------------+-----------+-------+-------------------------------+--------------+
	| Access key                    | Account     | Suspended | Type  | Owner (subuser or user)       | Permissions  |
	+-------------------------------+-------------+-----------+-------+-------------------------------+--------------+
	| jmktmpobj01usr001             | jmktmpobj01 | no        | S3    | jmktmpobj01:jmktmpobj01usr001 | full-control |
	| jmktmpobj01usr301             | jmktmpobj01 | no        | S3    | jmktmpobj01:jmktmpobj01usr301 | read         |
	| jmktmpobj01:jmktmpobj01usr001 | jmktmpobj01 | no        | Swift | jmktmpobj01:jmktmpobj01usr001 | full-control |
	| jmktmpobj01:jmktmpobj01usr301 | jmktmpobj01 | no        | Swift | jmktmpobj01:jmktmpobj01usr301 | read         |
	| flatmpobj01usr001             | flatmpobj01 | no        | S3    | flatmpobj01:flatmpobj01usr001 | full-control |
	| flatmpobj01usr301             | flatmpobj01 | no        | S3    | flatmpobj01:flatmpobj01usr301 | read         |
	| flatmpobj01:flatmpobj01usr001 | flatmpobj01 | no        | Swift | flatmpobj01:flatmpobj01usr001 | full-control |
	| flatmpobj01:flatmpobj01usr301 | flatmpobj01 | no        | Swift | flatmpobj01:flatmpobj01usr301 | read         |
	| costmpobj01                   | costmpobj01 | no        | S3    | costmpobj01                   | full-control |
	+-------------------------------+-------------+-----------+-------+-------------------------------+--------------+
	| Total : 9 key(s)              |             |           |       |                               |              |
	+-------------------------------+-------------+-----------+-------+-------------------------------+--------------+