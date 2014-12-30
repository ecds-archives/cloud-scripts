#!/usr/bin/python

import boto
from datetime import date, datetime, timedelta
import logging

# Array for tags
tags = ['Prod', 'Dev', 'beck-dev', 'PuppetMaster', 'Pitts', 'HBCUTours']

# Set up some logging
logging.basicConfig(filename='/var/root/cloud-scripts/snap.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Datetime objet
now = datetime.now()

# We want to keep 30 days worth of Prod snapshots but only 15 days
# of everything else. Here is where we calculate 30 days ago.
last_month = date.today() - timedelta(days=30)

# And here is where we calculate 15 days ago.
two_weeks_back = date.today() - timedelta(days=15)

# Start logging.
logging.info('Starting ' + now.strftime("%Y-%m-%d %H:%M"))

# Connect to the AWS API
ec2 = boto.connect_ec2()

# A function that finds the old snapshots and deletes them.
def delete_old_snaps(tag_name, old_date):
	old_snaps = ec2.get_all_snapshots(filters={'tag:Name': tag_name + ' ' + str(old_date) })

	for old_snap in old_snaps:
		logging.info('Deleteing ' + tag_name + ' ' + str(old_date) + ' ' + str(old_snap))
		old_snap.delete()

# This all assumes that the volumes are tagged with a name that is in the arrary "tags".
# This will iterate through the tags we specify, find the volumes that match and take
# an EBS snapshot of the volume. The resulting snapshot will be tagged with the name
# and the date in YYYY-MM-DD format.
for tag in tags:
	logging.info('Taking snaphshot of ' + tag)

	volumes = ec2.get_all_volumes(filters={'tag:Name': tag})

	snap = volumes[0].create_snapshot()

	snap.add_tag('Name', tag + ' ' + now.strftime("%Y-%m-%d"))

	if tag == 'Prod':
		delete_old_snaps(tag, last_month)
	else:
		delete_old_snaps(tag, two_weeks_back)

