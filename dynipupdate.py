#!/usr/bin/python

# https://USERNAME:PASSWORD@dynupdate.no-ip.com/nic/update?hostname=HOSTNAME

import urllib2
import urllib
import re
from os import path

ip_record_file = '/home/USERNAME/.ip-record'

# Fetches current IP
def getIP():
    ip_checker_url = "http://checkip.dyndns.org/"
    address_regexp = re.compile ('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    response = urllib2.urlopen(ip_checker_url).read()
    result = address_regexp.search(response)

    if result:
            return result.group()
    else:
            return None

# Real IP lookup
current_ip = getIP()

# Fetches previous IP or writes current IP to file
def previousIP():

    if path.isfile(ip_record_file):
        print "File exists. Reading old IP."
        f = open(ip_record_file, 'rw')
        return f.readline()
        f.close()
    else:
        print "File is missing. Creating file."
        f = open(ip_record_file, 'w')
        f.write(current_ip)
        f.close()
        return current_ip

# Fake IP lookup for test purposes
#current_ip = "127.0.0.1"

# Check last IP
previous_ip = previousIP()

# sanitize input from file
if previous_ip:
    previous_ip = previous_ip.rstrip()

# debug
print "Current IP:  " + current_ip
print "Previous IP: " + previous_ip

# Submit current IP to No-IP.com
def submitIP():
    ip_submission_url = "https://USERNAME:PASSWORD@dynupdate.no-ip.com/nic/update?hostname=HOSTNAME"
    response = urllib.urlopen(ip_submission_url).read()

    if response:
        print response
        return response
    else:
        return None

# Core logic
if current_ip == previous_ip:
    print "IP unchanged. Doing nothing."
elif previous_ip == None:
    print "No previous IP. Submitting current IP to No-IP.com."
    submitIP()
    f = open(ip_record_file, 'w')
    f.write(current_ip)
    f.close()
else:
    print "Submitting current IP to No-IP.com."
    submitIP()
    f = open(ip_record_file, 'w')
    f.write(current_ip)
    f.close()
