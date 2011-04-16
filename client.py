import os, time
import config

def load_data():
	data = []
	f = open(config.c['filename'], 'r')
	for line in f.readlines():
		data.append(line)
	f.close()
	return data

before = load_data()

while 1:
	time.sleep(30)
	after = load_data()
	diff = [line for line in after if not line in before]
	print diff
	before = after

