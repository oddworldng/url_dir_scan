import os
import sys
import json
import re

# Read gobuster output file (txt)
def read_gobuster_txt():

	file_to_read = open(gobuster_output_file, 'r')
	lines = file_to_read.readlines()
	
	paths = list()
	for line in lines:
		paths.append(line.split(" ")[0])
		
	return paths
	
# Read wfuzz output file (json)
def read_wfuzz_json(url):

	with open(wfuzz_output_file) as json_file:
		data = json.load(json_file)
	
	paths = list()
	for d in data:
		if d['code'] != 404:
			paths.append(d['url'].encode('ascii','ignore'))
	
	# Remove base URL from list
	try:		
		paths = list(set(paths)).remove(url)
	except ValueError:
		try:
			paths = list(set(paths)).remove(str('https://' + url + '/'))
		except ValueError:
			paths = list(set(paths)).remove(str('http://' + url + '/'))
	
	if paths is None:
		return "No dirs found"
	return paths


# Wordlist
#wordlist = "/usr/share/dirbuster/wordlists/directory-list-lowercase-2.3-medium.txt"
wordlist = "/usr/share/dirbuster/wordlists/directory-list-lowercase-2.3-small.txt"

# Output files
gobuster_output_file = "gobuster_output.txt"
wfuzz_output_file = "wfuzz_output"
dirb_output_file = "dirb_output.txt"

# Check if args
if len(sys.argv) > 1:

	# Get url from args
	url = sys.argv[1]
	
	# Run dirb
	print("Running dirb...")		
	
	# Check if url has http or https
	dirb_url = None
	if bool(re.match(r"http", url)) or bool(re.match(r"https", url)):
		dirb_url = url
	else: 
		dirb_url = "http://" + url
		
	os.system('dirb ' + dirb_url + ' ' + wordlist + ' -o ' + dirb_output_file + ' -f')
	
	# Read dirb output file (txt)
	
	# Remove dirb output file
	
	
	# Run gobuster
	print("\nRunning gobuster...")
	os.system('gobuster dir -q --url ' + url + ' --wordlist ' + wordlist + ' -o ' + gobuster_output_file)
	
	# Read gobuster output file (txt)
	output_gobuster = read_gobuster_txt()
	
	# Remove gobuster output file
	os.system('rm ' + gobuster_output_file)
	
	# Run wfuzz
	print("\nRunning wfuzz...")
	os.system('wfuzz -f wfuzz_output,json -w ' + wordlist + ' ' + url + '/FUZZ')
	
	# Read wfuzz output file (json)
	output_wfuzz = read_wfuzz_json(url)
	
	# Remove gobuster output file
	os.system('rm ' + wfuzz_output_file)
	
	# OUTPUS
	print("Gobuster... ")
	print(output_gobuster)
	
	print("Wfuzz... ")	
	print(output_wfuzz)
	
else:
	print("No arguments found")