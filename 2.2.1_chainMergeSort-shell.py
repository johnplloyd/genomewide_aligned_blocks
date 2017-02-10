print'''
inp1 = directory with .chain files
inp2 = output name
'''
import os,sys,fn

dir = os.path.abspath(sys.argv[1])
out_name = dir+"/"+sys.argv[2]
if not out_name.endswith(".chain.sorted"):
	out_name = out_name+".chain.sorted"

if os.path.isfile("chainMergeSort.sh") == True:
	chain_fl = fn.get_files(".","chainMergeSort")
	iteration = len(chain_fl)+1
	qsub_name = "chainMergeSort_%i.sh"%iteration
	shell = open(qsub_name,"w")
else:
	qsub_name = "chainMergeSort.sh"
	shell = open(qsub_name,"w")
shell.write('''#!/bin/bash -login
#PBS -q main
#PBS -l nodes=1:ppn=1,walltime=01:00:00,mem=1gb
/mnt/home/lloydjo1/bin/liftOver/chainMergeSort %s/*.chain.sorted.merged > %s
'''%(dir,out_name))
shell.close()
os.system("qsub %s"%qsub_name)
