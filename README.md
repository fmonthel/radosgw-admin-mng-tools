# Radosgw admin MNG Tools

Scripts to manage accounts, buckets, reporting for CEPH object mode (Swift and S3)

    pip install terminaltables rgwadmin argparse json

We're using radosgw-admin module (github)

##### Create account and keys :

    ./create-account.py -h

#####  Information on accounts :

    ./list-account.py -h

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
 
With example :
 
    ./list-buckets.py
    +--------------------+-------------+--------------+----------------------------+--------+-----------+---------+----------+--------+-------------+---------------+
    | Bucket name        | Owner       | Pool         | Created                    | Obj nb | Obj quota | GB size | GB quota | OPs nb | GB uploaded | GB downloaded |
    +--------------------+-------------+--------------+----------------------------+--------+-----------+---------+----------+--------+-------------+---------------+
    | jmktmpobj01buck003 | jmktmpobj01 | .rgw.buckets | 2015-10-29 05:19:25.000000 |      0 |         0 |     0.0 |      0.0 |      1 |         0.0 |           0.0 |
    | jmktmpobj01buck001 | jmktmpobj01 | .rgw.buckets | 2015-10-29 05:19:24.000000 |     96 |         0 |     4.9 |      0.0 |    520 |         4.8 |           0.0 |
    | flatmpobj01buck002 | flatmpobj01 | .rgw.buckets | 2015-11-01 22:57:51.000000 |      3 |         0 |     1.9 |      0.0 |    251 |         1.9 |           0.0 |
    | jmktmpobj01buck002 | jmktmpobj01 | .rgw.buckets | 2015-10-29 05:19:25.000000 |      0 |         0 |     0.0 |      0.0 |      1 |         0.0 |           0.0 |
    | flatmpobj01buck001 | flatmpobj01 | .rgw.buckets | 2015-10-29 05:13:27.000000 |    684 |         0 |     0.3 |      0.0 |    722 |         0.3 |           0.0 |
    +--------------------+-------------+--------------+----------------------------+--------+-----------+---------+----------+--------+-------------+---------------+
    | Total              |             |              |                            |    783 |         0 |     7.1 |      0.0 |   1495 |         7.1 |           0.0 |
    +--------------------+-------------+--------------+----------------------------+--------+-----------+---------+----------+--------+-------------+---------------+
