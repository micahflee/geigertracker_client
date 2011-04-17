import sys, os, datetime, time, hashlib, urllib, urllib2
import config

def load_data(filename):
	data = []
	f = open(filename, 'r')
	for line in f.readlines():
		data.append(line)
	f.close()
	return data

def generate_hash(count, timestamp):
	return hashlib.sha1(config.c['secret']+str(count)+str(timestamp)).hexdigest()

def parse_line(line):
	line = line.rstrip()
	date,sep,count = line.partition(' , ')
	timestamp = int(time.mktime(time.strptime(date, '%m/%d/%Y %I:%M:%S %p')))
	return timestamp,count

def update(line):
	timestamp,count = parse_line(line)
	if(timestamp != 0):
		timestamp_str = datetime.datetime.fromtimestamp(timestamp).strftime("%b %d %Y %H:%M:%S")
		print timestamp_str+"\t"+str(count)
		hash = generate_hash(count, timestamp)
		post_data = urllib.urlencode({'count':count, 'timestamp':timestamp, 'hash':hash})
		urllib2.urlopen(config.c['server_url'], post_data).read()

# if a filename is passed in, send data to server
if(len(sys.argv) > 1):
	filename = sys.argv[1]
	if(os.path.exists(filename)):
		print "Pushing data from "+filename+" to server"
		data = load_data(filename)
		for line in data:
			update(line)
	else:
		print "File "+filename+" does not exist"
	sys.exit()

# check for changes in radiation data file
print "Watching "+config.c['filename']+" for changes..."
before = load_data(config.c['filename'])
while 1:
	time.sleep(10)
	after = load_data(config.c['filename'])
	diff = [line for line in after if not line in before]
	
	for line in diff:
		update(line)

	before = after

