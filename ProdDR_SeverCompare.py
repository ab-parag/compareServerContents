#!/usr/bin/python2.6
'''
		Module1: Extract paths from PROD and DR servers
		Desc: 
			This is a code to extract entire directory structure under target path on a production server and store it in a file at user's home location. Then mail that file to User's mailbox. Similar code can be run on respective DR box and then user can compare both PROD and DR directory structure to identify gaps if any
		Inputs: 
			Target path
			User's home location
			User's mail address
		Output:
			Directory structure under target path (over mail)
'''
#Importing modules: import 'os' module from python library
import os	

#Declaration section: declare an empty list to hold all absolute paths
paths=[]

#Path extraction logic: append all extracted paths to 'paths' list and print total number of paths extracted
for path,dir,file in os.walk('/sys_apps/myapplication/data/'):
 paths.append(path)
print('total paths extracted: ' + str(len(paths)))

#check whether a desired directory is present at user's home path; if not present, create one and give appropriate permissions 
if not os.path.exists('/home/abParag/DR_preval/'):
 os.makedirs('/home/abParag/DR_preval/')
 os.system('chmod 777 /home/abParag/DR_preval/')

#go to the directory, create a file with hostname, timestamp and other details.
os.chdir('/home/abParag/DR_preval/')
os.system('touch /home/abParag/DR_preval/`hostname`_All_paths_`date "+%d-%m-%Y"`')
os.system('chmod 777 /home/abParag/DR_preval/`hostname`_All_paths_`date "+%d-%m-%Y"`')

#open the newly created file in 'append' mode and write the extracted paths list to it. Then close the file
file=os.listdir('/home/abParag/DR_preval/')[0]
f=open(file,'a')
for i in sorted(paths):
 f.write(str(i) + "\n")
f.close()

#tally if file is written by printing it's long listing details, and number of lines. Mail the file to given mail address
os.system('echo; ls -lrt /home/abParag/DR_preval/; echo; wc -l /home/abParag/DR_preval/`hostname`_prod_paths_`date "+%d-%m-%Y"`; echo;')
os.system('mailx -a /home/abParag/DR_preval/`hostname`_All_paths_`date "+%d-%m-%Y"` -s `hostname` ab.parag@gmail.com < /dev/null')
#Module1 Completed



'''
	Module2: Compare the PROD and DR files and write down missing paths in final.txt
	Desc: Assumption is that we've extracted paths from both PROD and DR box and have kept the files on same location where the code will run
	Input: 
		PROD file name
		DR file name
	Output:
		A results file having paths which are present in PROD but missing in DR
'''

#Open both the PROD and DR files and read them in to variables p and d respectively
with open('Server01_All_paths_26-05-2019','r') as prod, open('Server101_All_paths_26-05-2019','r') as dr:
	p=prod.readlines()
	d=dr.readlines()

#Compare the PROD file against DR and write down missing paths in 'results.txt'
with open('results.txt','w') as r:
	for i in p:
		if i not in d:
			r.write(i)

#remove duplicate paths if any from results.txt and write it to 'final.txt'
with open('results.txt','r') as r, open('final.txt','w') as f:
	rli=r.readlines()
	rli=list(dict.fromkeys(rli))
	f.writelines(rli)
#Module2 completed
	
	
	
	
'''
	Module3: Compare file checksums
	Desc: 
		this module will extract md5 value a files from the servers and prints the output to the console
	Input:
		File names of which the checksum is to be calculated
	Output:
		Exact file location/s on the server along with its checksum value
'''

#Interate through entire dorectory strusture under myapplication,  find the input file name and print it's checksum value along with it's absolute path
for path,dir,file in os.walk('/sys_apps/myapplication'):
 if ('MyApp.ini' in file):
  os.system('md5sum '+str(path)+'/MyApp.ini')
  
#like MyApp.ini we can compare any number of files. 
