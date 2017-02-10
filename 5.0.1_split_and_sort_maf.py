print'''
inp1 = MAF file
inp2 = number of species to include
inp3 = minimum alignment score
inp4 = output directory
inp5 = output prefix
'''
import os,sys,fn

maf_file = sys.argv[1]
species_num = int(sys.argv[2])
score_min = float(sys.argv[3])
out_dir = os.path.abspath(sys.argv[4])
prefix = sys.argv[5]

def maf2list(maf):
	inp = open(maf)
	all_l = []
	for line in inp:
		if not line.startswith("#"):
			if line.startswith("a"):
				short_l = []
				short_l.append(line.strip())
			elif line.startswith("s"):
				short_l.append(line.strip())
			elif line.strip() == "":
				all_l.append(short_l)
	inp.close()
	return all_l

def clean_string(str):
	while "  " in str:
		str = str.replace("  "," ")
	return str

def filter_sort_list(maf_l,spe_n,mn_score):
	dict = {}
	print "Filtering and reading into dictionary"
	for align in maf_l:
		num_spe = len(align)-1
		score = float(align[0].split("=")[-1])
		if num_spe >= spe_n and score >= mn_score:
			ref_list = clean_string(align[1]).strip().split(" ")
			chr_scaff = ref_list[1]
			location = int(ref_list[2])
			if chr_scaff not in dict:
				dict[chr_scaff] = []
			dict[chr_scaff].append([location,align])
	return dict

def sort_alignments(dict):
	print "Soring alignments by reference location"
	for chr_scaff in dict:
		alignments = dict[chr_scaff]
		alignments.sort(key=lambda k: (k[0]))

def write_output(dict,od,prfx):
	print "Writing output"
	for chr_scaff in dict:
		alignments = dict[chr_scaff]
		out = open("%s/%s-%s.maf"%(od,prfx,chr_scaff),"w")
		for align in alignments:
			out_str = "\n".join(align[1])
			out.write(out_str+"\n\n")
		out.close()	

maf_list = maf2list(maf_file)
chr_scaff_dict = filter_sort_list(maf_list,species_num,score_min)
sort_alignments(chr_scaff_dict)
write_output(chr_scaff_dict,out_dir,prefix)


# parse_maf(maf_file,species_num,score_min)

