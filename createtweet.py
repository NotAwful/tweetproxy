import optparse
from datetime import datetime

def writeout(key,value,outpath):
    outfile = open(outpath,'a')
    outfile.write(key + "," + value+"\n")
    outfile.close()

def main():
	parser = optparse.OptionParser('usage%prog '+'-t <time> -c <contents>')
	parser.add_option('-t','--time',
		dest="time",
		type='string',
		help="year,month,day,hour,minute")
	parser.add_option('-c','--content',
		dest="content",
		type='string',
		help="text content")
	(options, args) = parser.parse_args()
	if options.time == None:
		print parser.usage
		exit(0)
	elif options.time == "Now" or options.time == "now":
		posttime = str(datetime.now().isoformat())
	else:
		opttime = options.time.split(',')
		for item in range(5):
			opttime[item] = int(opttime[item])
		posttime = str(datetime(opttime[0],opttime[1],opttime[2],opttime[3],opttime[4]).isoformat())
	
	if options.content == None:
		print parser.usage
		exit(0)
	elif len(options.content) > 140:
		print "Tweet is " + str(len(options.content)) + " characters long. Tweets must be under 140 characters."
		exit(0)
	else:
		writeout(posttime,options.content,"./database.txt")
		print posttime + "," + options.content

if __name__ == '__main__':
	main()