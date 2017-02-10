print'''
inp1 = directory with target fasta files
inp2 = directory with query fasta files
inp3 = output directory
inp4 = runcc name
'''
import os,sys,fn

tar_dir = sys.argv[1]
query_dir = sys.argv[2]
out_dir = os.path.abspath(sys.argv[3])
runcc_name = sys.argv[4]

def parse_files_list(fl):
	l = []
	for item in fl:
		if item.endswith("nib") or item.endswith("sizes") or item.endswith("sizes_all"):
			pass
		else:
			l.append(item)
	return l

def get_parsed_files_list(d):
	fl = fn.get_files(d)
	pfl = parse_files_list(fl)
	return pfl

ptfl = get_parsed_files_list(tar_dir)
pqfl = get_parsed_files_list(query_dir)

if runcc_name.endswith(".runcc"):
	out = open(runcc_name,"w")
else:
	out = open(runcc_name+".runcc","w")

cnt = 0
for t_file in ptfl:
	for q_file in pqfl:
		cnt += 1
		command_line = "module load LASTZ;lastz %s %s > %s/tar-%s--\
query-%s.lav"%(t_file,q_file,out_dir,t_file.split("/")[-1],q_file.split("/")[-1])
		out.write(command_line+"\n")
out.close()

print "Number of pairwise alignments:",cnt
print "Alignments/300:",round(float(cnt)/300,1)
print "Alignments/200:",round(float(cnt)/200,1)
print "Alignments/100:",round(float(cnt)/100,1)