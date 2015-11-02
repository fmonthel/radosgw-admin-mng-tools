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
	+--------------+----------------------------------+--------------+---------------------+--------+---------+--------+-------------+---------------+
	| Account name | Display name                     | Bucket(s) nb | Max bucket(s) quota | Obj nb | GB size | OPs nb | GB uploaded | GB downloaded |
	+--------------+----------------------------------+--------------+---------------------+--------+---------+--------+-------------+---------------+
	| jmktmpobj01  | JMK TMP OBJECT ACCOUNT JMKELBERT |            3 |                1000 | 96     | 4.9     |    535 |         4.8 |           0.0 |
	| flatmpobj01  | FLA TMP OBJECT ACCOUNT FMONTHEL  |            2 |                1000 | 687    | 2.2     |   1192 |         4.0 |           1.9 |
	| costmpobj01  | COS ADMIN account                |            0 |                1000 | 0      | 0.0     |      0 |         0.0 |           0.0 |
	+--------------+----------------------------------+--------------+---------------------+--------+---------+--------+-------------+---------------+
	| Total        |                                  |            5 |                3000 | 783    | 7.1     |   1727 |         8.8 |           1.9 |
	+--------------+----------------------------------+--------------+---------------------+--------+---------+--------+-------------+---------------+

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
	+--------------------+-------------+--------------+----------------------------+--------+-----------+---------+----------+--------+-------------+---------------+
	| Bucket name        | Owner       | Pool         | Created                    | Obj nb | Obj quota | GB size | GB quota | OPs nb | GB uploaded | GB downloaded |
	+--------------------+-------------+--------------+----------------------------+--------+-----------+---------+----------+--------+-------------+---------------+
	| jmktmpobj01buck003 | jmktmpobj01 | .rgw.buckets | 2015-10-29 05:19:25.000000 |      0 |         0 |     0.0 |      0.0 |      1 |         0.0 |           0.0 |
	| jmktmpobj01buck001 | jmktmpobj01 | .rgw.buckets | 2015-10-29 05:19:24.000000 |     96 |         0 |     4.9 |      0.0 |    520 |         4.8 |           0.0 |
	| flatmpobj01buck002 | flatmpobj01 | .rgw.buckets | 2015-11-01 22:57:51.000000 |      3 |         0 |     1.9 |      0.0 |    252 |         1.9 |           1.9 |
	| jmktmpobj01buck002 | jmktmpobj01 | .rgw.buckets | 2015-10-29 05:19:25.000000 |      0 |         0 |     0.0 |      0.0 |      1 |         0.0 |           0.0 |
	| flatmpobj01buck001 | flatmpobj01 | .rgw.buckets | 2015-10-29 05:13:27.000000 |    684 |         0 |     0.3 |      0.0 |    722 |         0.3 |           0.0 |
	+--------------------+-------------+--------------+----------------------------+--------+-----------+---------+----------+--------+-------------+---------------+
	| Total              |             |              |                            |    783 |         0 |     7.1 |      0.0 |   1496 |         7.1 |           1.9 |
	+--------------------+-------------+--------------+----------------------------+--------+-----------+---------+----------+--------+-------------+---------------+
