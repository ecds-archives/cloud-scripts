cloud-scripts
=============

Repository for our various various scripts used for managing cloud servers and deployment of digital scholarship projects.

The scripts require the Boto Python library.

    pip install boto

In the home directory of the user that will run the scripts, crerate a file calle `.boto` and put the AWS keys in as follows:

    [Credentials]
    aws_access_key_id = <access key>
    aws_secret_access_key = <secret access key>

    [Boto]
    http_socket_timeout = 5

Here are the cron jobs used to run the scripts. Note the startstop.py does not run on the weekends.

    00 07,19 * * 1,2,3,4,5 /usr/bin/python /var/root/cloud-scripts/startstop.py
    00 22 * * * /usr/bin/python /var/root/cloud-scripts/snap.py
