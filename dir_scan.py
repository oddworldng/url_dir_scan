import os
import sys
import json
import re

# Wordlist
#wordlist = "/usr/share/dirbuster/wordlists/directory-list-lowercase-2.3-medium.txt"
wordlist = "/usr/share/dirbuster/wordlists/directory-list-lowercase-2.3-small.txt"

# Output files
gobuster_output_file = "gobuster_output.txt"
wfuzz_output_file = "wfuzz_output.json"
dirb_output_file = "dirb_output.txt"

# Remove base URL from list
def remove_base_url_from_list(paths, url):

	# Remove base URL from list
	try:		
		paths = list(set(paths)).remove(url)
	except ValueError:
		try:
			paths = list(set(paths)).remove(str('https://' + url + '/'))
		except ValueError:
			try:
				paths = list(set(paths)).remove(str('http://' + url + '/'))
			except ValueError:
				return paths
	return paths


# Read dirb output file (txt)
def read_dirb_txt(url):

	# Check if file exists
	try:
		file_to_read = open(dirb_output_file, 'r')
		lines = file_to_read.readlines()
	except IOError:
		print("No dirb file found: " + dirb_output_file)
		return list()
	
	# Read file
	paths = list()
	for line in lines:
		if bool(re.match(r"==> DIRECTORY: ", line)):
			paths.append(str(line.split('==> DIRECTORY: ')[1]).rstrip("\n"))
	
	# Remove base URL from list
	paths = remove_base_url_from_list(paths, url)
	
	return paths


# Read gobuster output file (txt)
def read_gobuster_txt():

	# Check if file exists
	try:
		file_to_read = open(gobuster_output_file, 'r')
		lines = file_to_read.readlines()
	except IOError:
		print("No gobuster file found: " + gobuster_output_file)
		return list()
	
	# Read file
	paths = list()
	for line in lines:
		paths.append(line.split(" ")[0])
		
	return paths


# Read wfuzz output file (json)
def read_wfuzz_json(url):

	# Check if file exists
	try:
		with open(wfuzz_output_file) as json_file:
			data = json.load(json_file)
	except IOError:
		print("No wfuzz file found: " + wfuzz_output_file)
		return list()
	
	paths = list()
	for d in data:
		if d['code'] != 404:
			paths.append(d['url'].encode('ascii','ignore'))
	
	# Remove base URL from list
	paths = remove_base_url_from_list(paths, url)
	
	if paths is None:
		return list()

	return paths


# Check if args
if len(sys.argv) > 1:

	# Get url from args
	url = sys.argv[1]
	
	
	# DIRB
	print("Running dirb...")		
	
	# Check if url has http or https
	dirb_url = None
	if bool(re.match(r"http", url)) or bool(re.match(r"https", url)):
		dirb_url = url
	else: 
		dirb_url = "http://" + url
		
	os.system('dirb ' + dirb_url + ' ' + wordlist + ' -o ' + dirb_output_file + ' -f')
	
	# Read dirb output file (txt)
	output_dirb = read_dirb_txt(url)
	
	# Remove dirb output file
	os.system('rm ' + dirb_output_file)
	
	
	# GOBUSTER
	print("\nRunning gobuster...")
	os.system('gobuster dir -q --url ' + url + ' --wordlist ' + wordlist + ' -o ' + gobuster_output_file)
	
	# Read gobuster output file (txt)
	output_gobuster = read_gobuster_txt()
	
	# Remove gobuster output file
	os.system('rm ' + gobuster_output_file)
	
	
	# WFUZZ
	print("\nRunning wfuzz...")
	os.system('wfuzz -f wfuzz_output,json -w ' + wordlist + ' ' + url + '/FUZZ')
	
	# Read wfuzz output file (json)
	output_wfuzz = read_wfuzz_json(url)
	
	# Remove gobuster output file
	os.system('rm ' + wfuzz_output_file)
	
	
	# OUTPUS
	print("\n\n\nDirb... ")
	if len(output_dirb) != 0:
		print(output_dirb)
	else:
		print(" [+] No dirs found")
	
	print("Gobuster... ")
	if len(output_gobuster) != 0:
		print(output_gobuster)
	else:
		print(" [+] No dirs found")
	
	print("Wfuzz... ")	
	if len(output_wfuzz) != 0:
		print(output_wfuzz)
	else:
		print(" [+] No dirs found")
		
else:
	print("No arguments found")