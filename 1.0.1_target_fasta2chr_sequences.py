print'''
inp1 = whole genome FASTA file
inp2 = output directory
'''
import os,sys,fn

fasta = sys.argv[1]
out_dir = os.path.abspath(sys.argv[2])

print "Reading FASTA file to dictionary..."
fasta_dict = fn.fasta2dict(fasta)
for key in fasta_dict:
	print "Writing chromosome/scaffold:",key
	seq_file_name = "%s.%s"%(fasta.split("/")[-1],key)
	out = open("%s/%s"%(out_dir,seq_file_name),"w")
	out.write(">%s\n"%seq_file_name)
	for seq_line in fasta_dict[key]:
		out.write(seq_line+"\n")
	out.close()
