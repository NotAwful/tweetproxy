import optparse, mechanize, cookielib
from datetime import datetime
from time import sleep
from os import remove as deletefile

def checkDB(queue,database):
	with open(database,'r') as file, open('./tmp.txt','w') as tempfile:
		for line in file:
			timestamp,tweet = line.split(',',1)
			tweet = tweet.rstrip('\n')
			if timestamp < datetime.now().isoformat():
				queue[timestamp] = tweet
			else:
				tempfile.write(line)
	with open(database,'w') as file, open('./tmp.txt','r') as source:
		for line in source:
			file.write(line)
	deletefile('./tmp.txt')

def main():
	parser = optparse.OptionParser('usage%prog '+'-u <username> -p <password> -d <database>')
	parser.add_option('-u','--username',
		dest="username",
		type='string',
		help="Twitter username")
	parser.add_option('-p','--password',
		dest="password",
		type='string',
		help="Twitter password")
	parser.add_option('-d','--database',
		dest="database",
		type='string',
		help="/path/to/tweet/database")
	(options, args) = parser.parse_args()
	if options.username == None or options.password == None:
		print parser.usage
		exit(0)
	username = options.username
	password = options.password
	if options.database == None:
		database = './database.txt'
	else:
		database = options.database

	br = mechanize.Browser()
	cookies = cookielib.LWPCookieJar()
	br.set_cookiejar(cookies)
	br.set_handle_equiv(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	br.set_debug_http(False)
	br.set_debug_responses(False)
	br.set_debug_redirects(False)
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time = 1)
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

	br.open('https://mobile.twitter.com/login')
	br.select_form(nr=1)
	br['session[username_or_email]'] = username
	br['session[password]'] = password
	br.submit()

	while True:
		queue = {}
		checkDB(queue,database)
		for key in queue.keys():
			target_url='/compose/tweet'
			for link in br.links():
	    			if link.url == target_url:        
	        			break
			br.follow_link(link)
			br.select_form(nr=1)
			br['tweet[text]'] = queue[key]
			queue.pop(key)
			br.submit()
			sleep(30)
		sleep(120)

if __name__ == '__main__':
	main()
