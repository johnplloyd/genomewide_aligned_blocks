print'''
inp1 = directory with fasta files
'''
import os,sys,fn

dir = sys.argv[1]

def parse_files_list(fl):
	l = []
	for item in fl:
		if item.endswith("lav") or item.endswith("psl") or item.endswith("nib") or item.endswith(".sizes"):
			pass
		else:
			l.append(item)
	return l

files_list = fn.get_files(dir)
pfl = parse_files_list(files_list)
for file in pfl:
	print "Working on file:",file
	command_line = "/mnt/home/lloydjo1/bin/liftOver/faSize %s -detailed > %s.sizes"%(file,file)
	os.system(command_line)
