#!/usr/bin/python

#Squeezebox related utilities

import pyjsonrpc
import json
import uuid
import pprint

def json_rpc( server_ip, command, player=''):
	# player  :=  The players mac address for commands that require a player
	# command :=  A slim command in the format of ["players",0,10]
	http_client = pyjsonrpc.HttpClient(url = "http://%s:9000/jsonrpc.js" % server_ip)
	return http_client.call("slim.request",player,command)
	
if __name__ == '__main__':
	pprint.pprint(json_rpc('192.168.10.4', ["players",0,10]))
	
	
	
