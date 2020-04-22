#!/usr/bin/python

import sys
from optparse import OptionParser
import urllib2
import json
import getpass
import os


URL = "http://%s:%s/%s"
gopts = {'host': 'localhost', 'no_passwd': True, 'ovx_user': 'admin', 'port': '8080'}

def do_getPhysicalTopology():
    gopts = {'host': 'localhost', 'no_passwd': True, 'ovx_user': 'admin', 'port': '8080'}
    req = {}
    result = connect(gopts, "status", "getPhysicalTopology", data=req, passwd="")
    return result


def connect(opts, path, cmd, data=None, passwd=None):
    try:
        url = getUrl(opts, path)
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, opts["ovx_user"], passwd)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        req = buildRequest(data, url, cmd)
        #ph = urllib2.urlopen(req)
        ph = opener.open(req)
        return parseResponse(ph.read())
    except urllib2.URLError as e:
        print e
        
    except urllib2.HTTPError as e:
        if e.code == 401:
            print "Authentication failed: invalid password"
            
        elif e.code == 504:
            print "HTTP Error 504: Gateway timeout"
            
        else:
            print e
    except RuntimeError as e:
        print "afskdfsd"+e

def getUrl(opts, path):
	return URL % (opts["host"], opts["port"], path)

def buildRequest(data, url, cmd):
    j = { "id" : "ovxctl",  "method" : cmd , "jsonrpc" : "2.0" }
    h = {"Content-Type" : "application/json-rpc"}  
    if data is not None:
        j['params'] = data
    return urllib2.Request(url, json.dumps(j), h)

def parseResponse(data):
    j = json.loads(data)
    if 'error' in j:
        print j
    try: 
    	return j['result'] 
    except KeyError:
    	return 0

def do_removeNetwork(args):
    req = { "tenantId" : int(args) }
    result = connect(gopts, "tenant", "removeNetwork", data=req, passwd="") 
    print "Network (tenant_id %s) has been removed" % (args)       

def do_listVirtualNetworks():
    req = {}
    result = connect(gopts, "status", "listVirtualNetworks", data=req, passwd="")
    return result


def do_createSwitch(args):
	opts = {'dpid': '0'}
	dpids = [int(dpid.replace(":", ""), 16) for dpid in args[1].split(',')]
	req = { "tenantId" : int(args[0]), "dpids" : dpids, "dpid" : int(opts["dpid"].replace(":", ""), 16) }
	reply = connect(gopts, "tenant", "createSwitch", data=req, passwd="")
	try:
		switchId = reply.get('vdpid')
		if switchId:
			switch_name = '00:' + ':'.join([("%x" % switchId)[i:i+2] for i in range(0, len(("%x" % switchId)), 2)])
	    	return switch_name
	except AttributeError:

		return 0

def do_createPort(args):
    req = { "tenantId" : int(args[0]), "dpid" : int(args[1].replace(":", ""), 16), "port" : int(args[2]) }
    reply = connect(gopts, "tenant", "createPort", data=req, passwd="")
    switchId = reply.get('vdpid')
    portId = reply.get('vport')
    if switchId and portId:
        switch_name = '00:' + ':'.join([("%x" %int(switchId))[i:i+2] for i in range(0, len(("%x" %int(switchId))), 2)])
        return (args[0], switch_name, portId)
    return 0


def do_connectLink(args):
    if len(args) != 7:
        print ("connectLink : Must specify tenant_id, src_virtual_dpid, src_virtual_port, dst_virtual_dpid, dst_virtual_port, " 
        + "algorithm (spf, manual), number of backup routes")
        sys.exit()
    req = { "tenantId" : int(args[0]), "srcDpid" : int(args[1].replace(":", ""), 16), 
           "srcPort" : int(args[2]), "dstDpid" : int(args[3].replace(":", ""), 16), 
           "dstPort" : int(args[4]), "algorithm" : args[5], "backup_num" : int(args[6]) }
    reply = connect(gopts, "tenant", "connectLink", data=req, passwd="")
    linkId = reply.get('linkId')
    if linkId:
        print "Virtual link (link_id %s) has been created" % (linkId)

def do_connectHost(args):
    req = { "tenantId" : int(args[0]), "vdpid" : int(args[1].replace(":", ""), 16),
            "vport" : int(args[2]), "mac" : args[3] }
    reply = connect(gopts, "tenant", "connectHost", data=req, passwd="")

    hostId = reply.get('hostId')
    if hostId:
        print "Host (host_id %s) has been connected to virtual port" % (hostId)




if __name__ == '__main__':

	a =  do_getPhysicalTopology()
	nets = do_listVirtualNetworks()
	for net in nets:
		do_removeNetwork(net)

	os.system("python ovxctl.py -n createNetwork tcp:10.0.0.3:10000 10.0.0.0 16")

	switches = {}
	virtual_ports = {'src' : 'v_src'}
	#print a['switches']
	s = a['switches']
	s.sort()
	print s
	for switch in s:
		v_src = do_createSwitch([1, switch])
		if v_src != 0:
			switches.update({switch : v_src })
			virtual_ports.update({switch : []})


	for link in a['links']:
		
		v_src_port = 0
		v_dst_port = 0
		src = link['src']['dpid']
		dst = link['dst']['dpid']
		v_src_port = do_createPort([1, src, link['src']['port']])

		if v_src_port != 0:
			virtual_ports[src].append({link['src']['port'] : v_src_port[2]})
			v_dst_port = do_createPort([1, dst, link['dst']['port'] ])  

		else: 
			continue

		if (v_dst_port != 0):
			virtual_ports[dst].append({link['dst']['port'] : v_dst_port[2]})
			print [1, switches[src], v_src_port[2], switches[dst], v_dst_port[2], "spf", 1]
			do_connectLink([1, switches[src], v_src_port[2], switches[dst], v_dst_port[2], "spf", 1])
		else:
			continue

		with open('v_dpids_map.json', 'w') as outfile:
			json.dump(switches, outfile)

		with open('v_ports_map.json', 'w') as outfile2:
			json.dump(virtual_ports, outfile2)

	with open('links.json', 'r') as linksfile:
		links = json.load(linksfile)
		for link in links:
			print link
			v_port_id = do_createPort([1, link["swich_dpid"], link["swich_port"]])
			do_connectHost([1, switches[link["swich_dpid"]], v_port_id[2], link["host_dpid"]])
