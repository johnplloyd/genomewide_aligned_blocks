print'''
inp1 = fasta file
inp2 = max size to break into
inp3 = output directory
'''
import os,sys,fn

# fasta_file = sys.argv[1].split("/")[-1]
fasta_file = sys.argv[1]
size = int(sys.argv[2])
out_dir = os.path.abspath(sys.argv[3])

def split_fasta(ff,sz,od):
	inp = open(ff)
	for line in inp:
		if line.startswith(">"):
			try:
				out.close()
			except:
				pass
			split_cnt = 1
			seq_length = 0
			# new_header = line.strip().replace(">",">%s_"%pf)
			sequence = line.strip().replace(">","")
			print "Working on chromosome/scaffold:",sequence
			seq_file_name = "%s.%s_%s"%(ff.split("/")[-1],sequence,split_cnt)
			out = open("%s/%s"%(od,seq_file_name),"w")
			out.write(">%s\n"%(seq_file_name))
		else:
			subseq = line.strip()
			if seq_length+len(subseq) <= sz:
				out.write(line)
				seq_length = seq_length+len(subseq)
			else:
				split_cnt += 1
				# out = open("%s/%s.%s_%s"%(od,ff,sequence,split_cnt),"w")
				seq_file_name = "%s.%s_%s"%(ff.split("/")[-1],sequence,split_cnt)
				out = open("%s/%s"%(od,seq_file_name),"w")
				out.write(">%s\n"%(seq_file_name))
				out.write(line)
				seq_length = len(subseq)
	inp.close()
	out.close()

split_fasta(fasta_file,size,out_dir)


"Sbic_Chr04_41.nib"