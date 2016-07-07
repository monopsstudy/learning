#!/usr/bin/python2.7

import os
import mmap


for root, dirnames, filenames in os.walk('./'):
#	print root;
#	print dirnames;
#	print filenames;
	for list_dir in dirnames:
		for root2, dirnames2, filenames2 in os.walk(list_dir):
#			print filenames2;
			for list_files in filenames2:
				with open(('./'+list_dir+'/'+list_files), 'r') as f:
					s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ);
#					print f;
					if s.find('joep') != -1:
						print list_files;
				f.closed;
