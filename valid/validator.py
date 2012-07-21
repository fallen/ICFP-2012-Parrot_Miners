#!/usr/bin/python
#import commands
import subprocess
import re
import string
import sys
#Invoke from repo root : ./valid/validator.py

def check_output(command):
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
	output = process.communicate()
	retcode = process.poll()
	if retcode:
		print output
		raise subprocess.CalledProcessError(retcode, command, output=output[0])
	return output

def test_map(mapname, route):
	route=route.strip()
	sed_stuff="sed -e \"s!.*Score: \(.*\)<br>.*!\\1!g\""
	cmd="curl -s http://undecidable.org.uk/~edwin/cgi-bin/weblifter.cgi --data 'mapfile="+mapname+"&route="+route+"' | grep -i score |"+sed_stuff
	cmd="curl -s http://undecidable.org.uk/~edwin/cgi-bin/weblifter.cgi --data 'mapfile="+mapname+"&route="+route+"'"
	returned_output=check_output(cmd)
	out=returned_output[0]
	r = re.compile(".*<pre>(.*)</pre>.*",re.DOTALL|re.MULTILINE)
	l = re.search(r,out)
	final_map= l.group(1)
	cmd="curl -s http://undecidable.org.uk/~edwin/cgi-bin/weblifter.cgi --data 'mapfile="+mapname+"&route="+route+"' | grep -i score |"+sed_stuff
	returned_output=check_output(cmd)
	out=returned_output[0]
	broken=False
	score="unset"
	if "Robot" in out:
		broken=True
		tab=out.split("<")
		score=tab[0]
	else:
		score=out.strip()
	print "---"
	print ""
	print "Map "+mapname
	print ""
	print final_map
	print "Route "+route
	if "complete" in score:
		print "Mining complete : got all lambdas \o/" #You rock
	score2=string.replace(score,"<br>"," ") # Remove nasty <br> on completion, do nothing otherwise
	print "Score = "+score2

	if broken:
		print "Robot broken"

if len(sys.argv) == 2:
	print "Running single map "+sys.argv[1]
	output=check_output("./valid/runmap.sh "+sys.argv[1])
	test_map(sys.argv[1],output[0])
	exit(0)


maps=[ "contest"+str(j) for j in range(1,11)]
#~ maps.extend(["flood"+str(i) for i in range(1,6)])
#~ maps.extend([ "trampoline"+str(k) for k in range(1,4)])
#~ maps.extend([ "horock"+str(k) for k in range(1,4)])
#~ maps.extend([ "beard"+str(k) for k in range(1,6)])
for m in maps:
	output=check_output("./valid/runmap.sh "+m)
	test_map(m,output[0])
