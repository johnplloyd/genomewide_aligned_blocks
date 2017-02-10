print'''
inp1 = maf file 1
inp2 = maf file 2
inp3 = output name
'''
import os,sys,fn

maf1 = os.path.abspath(sys.argv[1])
maf2 = os.path.abspath(sys.argv[2])
out_nm = os.path.abspath(sys.argv[3])

if os.path.isfile("multiz_submit.sh") == True:
	chain_fl = fn.get_files(".","multiz_submit")
	iteration = len(chain_fl)+1
	qsub_name = "multiz_submit%i.sh"%iteration
	shell = open(qsub_name,"w")
else:
	qsub_name = "multiz_submit.sh"
	shell = open(qsub_name,"w")
shell.write('''#!/bin/bash -login
#PBS -q main
#PBS -l nodes=1:ppn=1,walltime=01:00:00,mem=1gb
/mnt/home/lloydjo1/bin/multiz-tba.012109/multiz %s %s v > %s
'''%(maf1,maf2,out_nm))
shell.close()
os.system("qsub %s"%qsub_name)