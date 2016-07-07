#!/usr/bin/python26
"""
It is task for filesystems lesson. This script finds all files with text 'joep' by default inside and print theirs filename. Print only files and files can be in different directories under root (grants/) directory 
Author: Olha Honcharuk 06/07/16
"""
from optparse import OptionParser
from datetime import datetime, timedelta
import os
import mmap
import re
import time
import sys

parser = OptionParser()
parser.add_option('-w', '--way', action='store_true', dest='hostname', default=False, 
					help='Print only hostnames from filenames')
parser.add_option('-y', '--yesterday', action='store_true', dest='yesterday_hostname', default=False, 
					help='Get hostname only from files created yesterday')
parser.add_option('-n', '--name', dest='name', type='str',default='joep',
					help='Name which shold be searched in files [Default: joep]')

opts, args = parser.parse_args()


class FindFiles:
	"""
	Class for finding all files in root (grants/) directory which consist some name
	"""
	def __init__(self, hostname,yesterday_hostname,name):
		self.hostname=hostname
		self.yesterday_hostname=yesterday_hostname
		self.name=name

	def modified_yesterday(self,file):
		"""
		Indicates if file was last modified yesterday
		:return: was_modified
		"""
		try:
			today = datetime.now().date()
			yesterday = today - timedelta(1)
			unix_today=time.mktime(today.timetuple())
			unix_yesterday=time.mktime(yesterday.timetuple())
			file_date=os.stat(file).st_mtime
			if unix_yesterday<=file_date<unix_today:
				was_modified=True
			else:
				was_modified=False
		except Exception as e:
			was_modified=False
			print "Error is: %s" %e
		return was_modified

	def get_hostname(self,file):
		"""
		Extracts a hostname from file
		:return: hostname
		"""
		try:
			reg=re.search('grants-(.*).out.*',file)
			if reg:
				hostname=reg.group(1)
			else:
				hostname=""
		except Exception as e:
			hostname=""
			print "Error is: %s" %e
		return hostname

	def main(self):
		"""
		Main function, finding file with some name
		:return: exit_code
		"""
		try:
			ROOT_DIR = os.getcwd()
			for root,dirs,files in os.walk(ROOT_DIR):
				for file in files:
					with open(root+'/'+file,'rb') as data_read_file:
						regex_str=mmap.mmap(data_read_file.fileno(),0,access=mmap.ACCESS_READ)
						if re.search(r'\b({0})\b'.format(self.name),regex_str):
							if self.yesterday_hostname:
								if self.modified_yesterday(root+'/'+file):
									print self.get_hostname(file)
							elif self.hostname:
								print self.get_hostname(file)
							else:
								print file
			exit_code=0
		except Exception as e:
			exit_code=2
			print "Error is: %s" %e
		return exit_code

if __name__ == '__main__':
	start_finding=FindFiles(opts.hostname,opts.yesterday_hostname,opts.name)
	exit_code=start_finding.main()
	sys.exit(exit_code)

