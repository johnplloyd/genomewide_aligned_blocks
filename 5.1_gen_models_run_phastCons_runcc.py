print'''
inp1 = directory with maf and mod files
inp2 = Newick tree file
inp3 = output stump
'''
import os,sys,fn

dir = sys.argv[1]
newick = os.path.abspath(sys.argv[2])
out_nm = sys.argv[3]

def copy_tree__write_runccs(tree,fl,m_runcc,p_runcc):
	new_tree = "%s.%s.nwk"%(tree,fl.split("/")[-1].replace(".maf",""))
	copy_command = "cp %s %s"%(tree,new_tree)
	os.system(copy_command)
	model_command = "module load PHAST;phastCons -i MAF --estimate-trees %s --no-post-probs %s %s.mod\n"%\
(new_tree,fl,fl)
	m_runcc.write(model_command)
	phastCons_command = "module load PHAST;phastCons -i MAF %s %s.cons.mod,%s.noncons.mod > %s.wig\n"%\
(fl,new_tree,new_tree,fl)
	p_runcc.write(phastCons_command)

files_list = fn.get_files(dir,".maf","tail")
model_runcc = open(out_nm+"-generate_models.runcc","w")
phastCons_runcc = open(out_nm+"-run_phastCons.runcc","w")
for file in files_list:
	copy_tree__write_runccs(newick,file,model_runcc,phastCons_runcc)
model_runcc.close()
phastCons_runcc.close()
