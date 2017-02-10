print'''
inp1 = directory with .psl files
inp2 = directory with target .nib files
inp3 = directory with query .nib files
inp4 = output for .chain files
'''
import os,sys,fn

dir = sys.argv[1]
t_nib_dir = os.path.abspath(sys.argv[2])
q_nib_dir = os.path.abspath(sys.argv[3])
out_dir = os.path.abspath(sys.argv[4])

if os.path.isfile("chain_psl.sh") == True:
	chain_fl = fn.get_files(".","chain_psl")
	iteration = len(chain_fl)+1
	qsub_name = "chain_psl_%i.sh"%iteration
	shell = open(qsub_name,"w")
	
else:
	qsub_name = "chain_psl.sh"
	shell = open(qsub_name,"w")

shell.write('''#!/bin/bash -login
#PBS -q main
#PBS -l nodes=1:ppn=1,walltime=03:59:00,mem=1gb
''')

files_list = fn.get_files(dir,".psl","tail")
for file in files_list:
	command_line = "/mnt/home/lloydjo1/bin/liftOver/axtChain -linearGap=\
medium -psl %s %s %s %s/%s\n"%(file,t_nib_dir,q_nib_dir,out_dir,file.split\
("/")[-1].replace(".psl",".chain"))
	# print command_line
	# os.system(command_line)
	shell.write(command_line)

shell.close()
os.system("qsub %s"%qsub_name)