print'''
inp1 = directory with fasta files
'''
import os,sys,fn

dir = sys.argv[1]

def parse_files_list(fl):
	l = []
	for item in fl:
		if item.endswith("nib") or item.endswith(".sizes"):
			pass
		else:
			l.append(item)
	return l

files_list = fn.get_files(dir)
parsed_fl = parse_files_list(files_list)
for file in parsed_fl:
	print "Working on file:",file
	command_line = "/mnt/home/lloydjo1/bin/liftOver/faToNib %s %s.nib"%(file,file)
	os.system(command_line)
