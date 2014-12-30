CloudScripts
============

Collection of scripts to mange AWS resources by starting and stopping instances and taking EBS snapshots of EBS volumes.

Repuirments
-----------

The scripts require the Boto Python library.

    pip install boto

In the home directory of the user that will run the scripts, crerate a file calle `.boto` and put the AWS keys in as follows:

    [Credentials]
    aws_access_key_id = <access key>
    aws_secret_access_key = <secret access key>

    [Boto]
    http_socket_timeout = 5

startstop.py
------------

This script has a list of EC2 instance IDs. It will start each instance at 7am and attach its Elastic IP. The script will stop each in the list instance at 7pm.

snap.py
-------

This script takes EBS snapshots (block level incremental backup) based on volume tags. Production level snapshots are retained for one month. Development level snapshots are retained for two weeks.

Crontab Example
--------------- 

Here are the cron jobs used to run the scripts. Note the startstop.py does not run on the weekends.

    00 07,19 * * 1,2,3,4,5 /usr/bin/python /path/to/startstop.py
    00 22 * * * /usr/bin/python /path/to/snap.py
