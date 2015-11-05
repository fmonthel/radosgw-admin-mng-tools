# Radosgw admin MNG Tools

Scripts to manage accounts, buckets, reporting for Ceph object mode (Swift and S3)

    pip install terminaltables rgwadmin argparse

We're using radosgw-admin module (github)

##### Create account and keys :

    ./create-account.py -h

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
	+----------------------+----------------------------------+-----------+--------------+---------------+--------+---------+--------------+--------------+------------+-----------+
	| Account name         | Display name                     | Suspended | Bucket(s) nb | Max bucket(s) | Obj nb | GB size | OP(s) OK (*) | OP(s) KO (*) | GB upl (*) | GB dl (*) |
	+----------------------+----------------------------------+-----------+--------------+---------------+--------+---------+--------------+--------------+------------+-----------+
	| jmktmpobj01          | JMK TMP OBJECT ACCOUNT JMJMJMJMJ | no        |            3 |          1000 |     96 |     4.9 |          535 |            1 |        4.8 |       0.0 |
	| flatmpobj01          | FLA TMP OBJECT ACCOUNT FMONTHEL  | yes       |            2 |          1000 |    696 |     2.3 |         1204 |            1 |        4.0 |       1.9 |
	| costmpobj01          | COS ADMIN account                | no        |            0 |          1000 |      0 |     0.0 |            0 |            0 |        0.0 |       0.0 |
	+----------------------+----------------------------------+-----------+--------------+---------------+--------+---------+--------------+--------------+------------+-----------+
	| Total : 3 account(s) |                                  |           |            5 |          3000 |    792 |     7.2 |         1739 |            2 |        8.8 |       1.9 |
	+----------------------+----------------------------------+-----------+--------------+---------------+--------+---------+--------------+--------------+------------+-----------+
	* Stats from 2015-10-28 04:00:00 to 2015-11-04 20:00:00
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