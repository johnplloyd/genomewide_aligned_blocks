
def print_help():
	print'''
inp1 = Directory with wig score files
	(should also include maf files)
inp2 = Output name prefix
'''

def parse_wig(fl):
	inp = open(fl)
	pC_dict = {}
	for line in inp:
		if line.startswith("fixedStep"):
			lineLst = line.strip().split(" ")
			index = lineLst[-2].replace("start=","")
			pC_dict[index] = []
		else:
			pC_dict[index].append(line.strip())
	return pC_dict

def parse_maf(fl):
	inp = open(fl)
	begin = True
	maf_dict = {}
	for line in inp:
		if line.startswith("a"):
			lineLst = line.strip().split(" ")
			score = lineLst[1].replace("score=","")
			if begin == True:
				begin = False
				aln_list = []
			else:
				index = aln_list[0][2]
				index_tup = (index,score)
				maf_dict[index_tup] = aln_list
				aln_list = []
			
		elif line.startswith("s"):
			clean_line = fn.clear_spaces(line)
			# print
			# print clean_line
			lineLst = clean_line.split("\t")
			# print lineLst
			aln_list.append(lineLst)
	return maf_dict

def retrieve_pC_score(aln_curr,pC_d,key):
	dashed_score = []
	non_dashed = pC_d[key]
	cnt = 0
	if "-" in aln_curr:
		for col in aln_curr:
			if col == "-":
				dashed_score.append("-")
			else:
				dashed_score.append(non_dashed[cnt])
				cnt += 1
	else:
		dashed_score = pC_d[key]
	float_sc=fn.make_float_list(non_dashed)
	total = sum(float_sc)
	average = round(total/len(float_sc),3)
	med_scr = fn.median(float_sc)
	return dashed_score,non_dashed,med_scr,average

def subblock_locations(align_list):
	block_list = range(0,len(align_list[0][-1]))
	for align in align_list:
		ind = 0
		aln_seq = align[-1]
		for col in aln_seq:
			if col == "-":
				if ind in block_list:
					block_list.remove(ind) 
			ind+=1
	
	block_coords = []
	subblock_start = block_list[0]
	subblock_end = ""
	for i in range(0,len(block_list)-1):
		if block_list[i]+1 != block_list[i+1]:
			subblock_end = block_list[i]
			block_coords.append([subblock_start,subblock_end])
			
			subblock_start=block_list[i+1]
			subblock_end = ""
	block_coords.append([subblock_start,block_list[-1]])
	return block_coords

# def remove_qry_dashes(tar_dashed_score,qry_aln_list,full_aln_list,blck_nm):
# def remove_qry_dashes(tar_dashed_score,qry_aln_list):
def remove_qry_dashes(tar_dashed_score,aln_seq_list):
	# aln_seq_list = list(qry_aln_list[-1])
	matched_score = []
	if len(tar_dashed_score) == len(aln_seq_list):
		for i in range(0,len(tar_dashed_score)):
			seq_char = aln_seq_list[i]
			if seq_char != "-":
				matched_score.append(tar_dashed_score[i])
	else:
		print
		print
		print "DIFFERENT LENGTHS        DIFFERENT LENGTHS        DIFFERENT LENGTHS        DIFFERENT LENGTHS        DIFFERENT LENGTHS"
		# print blck_nm
		# print qry_aln_list[1]
		# for item in full_aln_list:
			# print item
		print len(tar_dashed_score),len(aln_list)
	return matched_score

def gff(pC_d,maf_d,d,prefix,bl_num,begin):
	bg_cnt = 1
	total_ind = len(maf_d)
	for index_alnSc_pair in maf_d:
		if bg_cnt%500 == 0:
			print "        On index # %s of %s"%(bg_cnt,total_ind)
		aln_l=maf_d[index_alnSc_pair]
		block_coordinates = subblock_locations(aln_l)
		index,alnSc = index_alnSc_pair
		wig_ind = str(int(index)+1)
		if wig_ind in pC_d:
			tar_aln_seq = aln_l[0][-1]
			tar_noDash_seq = tar_aln_seq.replace("-","")
			tar_dash_score,tar_nonDash_score,median_scr,ave_sc = retrieve_pC_score(tar_aln_seq,pC_d,wig_ind)
			if begin == True:
				for aln in aln_l:
					species = aln[1].split(".")[0]
					open(d+"/"+prefix+"-"+species+".phastCons_summary","w")
					file(d+"/"+prefix+"-"+species+".phastCons_summary","a").write("#block\tfile\tfasta_seq\tstart\tend\tstrand\tlen\taln_sc\tave_sc\tmed_sc\talignment\tphastCons_scores\n")
					# open(d+"/"+prefix+"-"+species+".full_block_locations.gff","w")
					# open(d+"/"+prefix+"-"+species+".sub_block_locations.gff","w")
				begin = False
			if len(tar_noDash_seq) == len(tar_nonDash_score):
				for aln in aln_l:
					strand = aln[4]
					# print strand
					aln_seq = aln[-1]
					aln_noDash_seq = aln_seq.replace("-","")
					species = aln[1].split(".")[0]
					# print species
					# print aln_seq
					# print
					file_seq = aln[1]
					file_seq_l = file_seq.split(".")
					file_nm = ".".join(file_seq_l[0:-1])
					seq = file_seq_l[-1]
					if "_" in seq:
						seq_l = seq.split("_")
						seq = "_".join(seq_l[0:-1])
						chunk = int(seq_l[-1])
						start = int(aln[2])+(1000000*(chunk-1))+1
					else:
						start = int(aln[2])+1
					end = start+int(aln[3])-1
					length=end-start+1
					
					aln_seq_list = list(aln_seq)
					aln_seq_str=",".join(aln_seq_list)
					dash_scr_str=",".join(tar_dash_score)
					
					# qry_matched_score = remove_qry_dashes(tar_dash_score,aln,aln_l,bl_num)
					# qry_matched_score = remove_qry_dashes(tar_dash_score,aln_seq_list)
					# if len(qry_matched_score) != len(aln_noDash_seq):
						# print "Something's screwey"
					# qry_matched_score_str = ",".join(qry_matched_score)
					
					out_str="%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(bl_num,file_nm,seq,start,end,strand,length,alnSc,ave_sc,median_scr,aln_seq,dash_scr_str)
					file(d+"/"+prefix+"-"+species+".phastCons_summary","a").write(out_str)
					
					# description="block_ID=%s;feature=syntenic_block;length=%s;sequence=%s;phastCons_str=%s"%(bl_num,length,aln_noDash_seq,qry_matched_score_str)
					# gff_line_string = "%s\tsyntenic_block\tsyntenic_block\t%s\t%s\t.\t.\t.\t%s\n"%(seq,start,end,description)
					# file(d+"/"+prefix+"-"+species+".full_block_locations.gff","a").write(gff_line_string)
					
					sub_bl_num = bl_num
					for coords in block_coordinates:
						# print "working on subcoords"
						sub_bl_num+=0.001
						if len(str(sub_bl_num)) == 11:
							sub_bl_num_str = str(sub_bl_num)
						elif len(str(sub_bl_num)) == 10:
							sub_bl_num_str = str(sub_bl_num)+"0"
						elif len(str(sub_bl_num)) == 9:
							sub_bl_num_str = str(sub_bl_num)+"00"
						# sub_scores = fn.make_float_list(tar_dash_score[coords[0]:coords[1]+1])
						
						sub_score_lst = tar_dash_score[coords[0]:coords[1]+1]
						sub_score_str = ",".join(sub_score_lst)
						
						sub_aln = aln_seq[coords[0]:coords[1]+1]
						sub_aln_lst = list(sub_aln)
						sub_aln_str = ",".join(sub_aln_lst)
						sub_noDash_aln = ",".join(sub_aln_lst).replace("-","")
						
						fl_sub_scores = fn.make_float_list(sub_score_lst)
						sub_total_sc = sum(fl_sub_scores)
						sub_ave_sc = round(sub_total_sc/len(fl_sub_scores),3)
						sub_med_sc = fn.median(fl_sub_scores)
						
						sub_start=int(start)+coords[0]
						sub_end=int(start)+coords[1]
						sub_len=sub_end-sub_start+1
						sub_out_str="%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(sub_bl_num_str,file_nm,seq,sub_start,sub_end,strand,sub_len,"NA",sub_ave_sc,sub_med_sc,sub_aln,sub_score_str)
						file(d+"/"+prefix+"-"+species+".phastCons_summary","a").write(sub_out_str)
						
						
						# sub_qry_matched_score = remove_qry_dashes(sub_score_lst,sub_aln_lst)
						# sub_qry_matched_score_str = ",".join(sub_qry_matched_score)
						
						# subdesc="block_ID=%s;feature=syntenic_block_nonGapped_subregion;length=%s;sequence=%s;phastCons_str=%s"%(sub_bl_num,sub_len,sub_noDash_aln,sub_qry_matched_score_str)
						# gff_sub_string = "%s\tsyntenic_subblock\tnonGapped_subblock\t%s\t%s\t.\t.\t.\t%s\n"%(seq,sub_start,sub_end,subdesc)
						# file(d+"/"+prefix+"-"+species+".sub_block_locations.gff","a").write(gff_sub_string)
						
						# sub_out_str="%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(sub_bl_num_str,file_nm,seq,sub_start,sub_end,sub_total_sc,sub_ave_sc)
						
				bl_num += 1
		bg_cnt += 1
	return bl_num,begin

def main():
	import os,sys
	if len(sys.argv) == 1 or "-h" in sys.argv:
		print_help()
		sys.exit()
	
	try:
		dir = os.path.abspath(sys.argv[1])
		out_nm = sys.argv[2]
	except:
		print_help()
		print "Error reading arguments, quitting!"
		sys.exit()
	
	files_list = fn.get_files(dir,"wig","tail")
	block_number = 1000000
	begin_command = True
	fl_cnt = 1
	for wig in files_list:
		maf = wig.replace(".wig","")
		
		print "\nFile %s of %s: %s"%(fl_cnt,len(files_list),wig)
		print "  Parsing maf file"
		maf_dict = parse_maf(maf)
		print "  Parsing wig file"
		phastCons_dict = parse_wig(wig)
		print "  Creating gff coordinates and writing to output"
		
		block_number,begin_command = gff(phastCons_dict,maf_dict,dir,out_nm,block_number,begin_command)
		fl_cnt += 1

if __name__ == "__main__":
	import fn
	main()
