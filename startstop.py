#!/usr/bin/python

import boto
import time
import datetime
import logging

'''
This script starts up our dev server every morning at 7am and shuts
it down again at 7pm. Here is an example cron entry that runs the
script on weekdays at 7am and 7pm:

00 07,19 * * 1,2,3,4,5 /usr/bin/python /path/to/startstop.py
'''

dev_id = 'i-5a18ab20'
dev_ip = '23.21.175.158'

logging.basicConfig(filename='startstop.log',level=logging.INFO)

ec2 = boto.connect_ec2()

now = datetime.datetime.now()

logging.info('Start run: ' + now.strftime("%Y-%m-%d %H:%M"))

if now.hour == 7:
	logging.info('Starting Dev')
	ec2.start_instances(instance_ids=[dev_id])

	reservations = ec2.get_all_instances()

	instances = [i for r in reservations for i in r.instances]
	
	for i in instances:
		if i.id == dev_id:
			status = i.update()
			while status == 'pending':
				logging.info('Waiting for instance to start')
				time.sleep(10)
				status = i.update()
			if i.state == 'running':
				logging.info('Setting IP')
				ec2.associate_address(dev_id, dev_ip)

elif now.hour == 19:
	logging.info('Stopping Dev')
	ec2.stop_instances(instance_ids=[dev_id])

else:
	logging.info('Nothing to do')

logging.info('Stop run: ' + now.strftime("%Y-%m-%d %H:%M"))
