#!/usr/bin/python

import boto
import datetime
import logging

tags = ['Prod', 'Dev', 'Puppet']

logging.basicConfig(filename='snap.log',level=logging.INFO)

now = datetime.datetime.now()

logging.info(now.strftime("%Y-%m-%d %H:%M"))

ec2 = boto.connect_ec2()

for tag in tags:
	logging.info('Taking snaphshot of ' + tag)

	volumes = ec2.get_all_volumes(filters={'tag:Name': tag})

	snap = volumes[0].create_snapshot()

	snap.add_tag('Name', tag + now.strftime("%Y-%m-%d"))
