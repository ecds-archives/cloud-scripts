cloud-scripts
=============

Repository for our various various scripts used for managing cloud servers and deployment of digital scholarship projects.

Here are the cron jobs used to run the scripts. Note the startstop.py does not run on the weekends.

    00 07,19 * * 1,2,3,4,5 /usr/bin/python /var/root/cloud-scripts/startstop.py
    00 22 * * * /usr/bin/python /var/root/cloud-scripts/snap.py
