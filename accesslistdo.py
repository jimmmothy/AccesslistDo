#!/usr/bin/python3

'''
Requires geoiplookup
Parses denied SSH/Telnet attempts picked up by rsyslog/syslog-ng to show percentage of offender by country

Example of syslog messages sent by Cisco router
Sep 26 12:13:08 192.168.0.1 %SEC-6-IPACCESSLOGP: list 100 denied tcp 107.189.8.8(58282) -> x.x.x.x(22), 1 packet
'''

import re
import time
import subprocess


def main():

	rsyslogfile = 'cisco.log'
	datasrc = open(rsyslogfile, 'r')
	data = datasrc.readlines()
	culprits = []

	for x in data:
		reg = re.findall("[a-zA-Z]+[ ][\d]+[ ][0-9:]+[ ][\d.]+[ ](%SEC-6-IPACCESSLOGP): list [\d]+[ ](denied tcp)[ ]([\d.]+)\(([\d]+)\)\s->\s([\d.]+)\(([\d]+)\)",x)
		if reg:
			s_ip = reg[0][2]
			culprits.append(s_ip)

	counter = {}
	totalattempts = 0
	percentdone = 0
	fivepercent = int(len(culprits) / 20)
	print(f"running geoiplookup.. { len(culprits) } entries to do")

	for x in culprits:
		totalattempts += 1
		bashCommand = "geoiplookup " + x

		process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
		out, error = process.communicate()

		country = str(out)[25:-3]
		if country not in counter:
			counter[country] = 1
		else:
			counter[country] += 1
		
		# This can take a while, so added a counter
		if totalattempts % fivepercent == 0:
			percentdone += 5
			print(f"{ percentdone }%")

	print("Complete...")
	time.sleep(2)
	process = subprocess.Popen("clear", stdout=subprocess.PIPE)

	counterl = sorted(counter.items(), key=lambda x:x[1])
	scounter = dict(counterl)

	for z in scounter:
		rawpercent = (scounter[z] / totalattempts)*100
		fpercent = format(rawpercent, '.2f')
		print(f"{ z }, { scounter[z] } : { fpercent }%")


if __name__ == '__main__':
	main()