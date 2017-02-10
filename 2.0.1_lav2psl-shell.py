print'''
inp1 = directory with .lav files
inp2 = output directory for .psl files
'''
import os,sys,fn

dir = sys.argv[1]
out_dir = os.path.abspath(sys.argv[2])

if os.path.isfile("lav2psl.sh") == True:
	chain_fl = fn.get_files(".","chain_psl")
	iteration = len(chain_fl)+1
	qsub_name = "lav2psl_%i.sh"%iteration
	shell = open(qsub_name,"w")
else:
	qsub_name = "lav2psl.sh"
	shell = open(qsub_name,"w")
shell.write('''#!/bin/bash -login
#PBS -q main
#PBS -l nodes=1:ppn=1,walltime=02:00:00,mem=1gb
''')
files_list = fn.get_files(dir,".lav","tail")
for file in files_list:
	command_line = "/mnt/home/lloydjo1/bin/liftOver/lavToPsl %s %s/%s\n"%(file,out_dir,file.split("/")[-1].replace("lav","psl"))
	# os.system(command_line)
	shell.write(command_line)
shell.close()
os.system("qsub %s"%qsub_name)
