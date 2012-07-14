#!/usr/bin/python
#import commands
import subprocess

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
	print "Map "+mapname
	print "Route "+route
	print "Score = "+score
	if broken:
		print "Robot broken"

maps=["flood"+str(i) for i in range(1,6)]
maps.extend([ "contest"+str(j) for j in range(1,11)])

for m in maps:
	output=check_output("./valid/runmap.sh "+m)
	test_map(m,output[0])
