#!/usr/bin/python

import boto
from datetime import date, datetime, timedelta
import logging

tags = ['Prod', 'Dev', 'Puppet']

logging.basicConfig(filename='/var/root/cloud-scripts/snap.log',level=logging.INFO)

now = datetime.now()

last_month = date.today() - timedelta(days=30)

two_weeks_back = date.today() - timedelta(days=15)

logging.info(now.strftime("%Y-%m-%d %H:%M"))

ec2 = boto.connect_ec2()

def delete_old_snaps(tag_name, old_date):
	old_snaps = ec2.get_all_snapshots(filters={'tag:Name': tag_name + ' ' + str(old_date) })

	for old_snap in old_snaps:
		logging.info('Deleteing ' + tag_name + ' ' + str(old_date) + ' ' + str(old_snap))
		old_snap.delete()

for tag in tags:
	logging.info('Taking snaphshot of ' + tag)

	volumes = ec2.get_all_volumes(filters={'tag:Name': tag})

	snap = volumes[0].create_snapshot()

	snap.add_tag('Name', tag + ' ' + now.strftime("%Y-%m-%d"))

	if tag == 'Prod':
		delete_old_snaps(tag, last_month)
	else:
		delete_old_snaps(tag, two_weeks_back)

