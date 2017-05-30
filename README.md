# tweetproxy
A tool for proxying or scheduling tweets via command line.
## Usage
1. Run tweetproxy as a background job.
```
python .\tweetproxy.py -u 420blazeit6969 -p p@ssw0rd -d '\home\john\tweetproxy\database.txt' &
```
2. use createtweet to add tweets to the database to be posted at a later date.
```
python .\createtweet.py -t 2018,04,20,0,0 -c 'It's my birthday! <3'
python .\createtweet.py -t now -c 'Something something xxSephiroth420xx'
```
