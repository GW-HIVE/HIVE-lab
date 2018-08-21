import os,sys
import string
from optparse import OptionParser
from Bio import SeqIO
import glob
import MySQLdb
import csv


__version__="1.0"
__status__ = "Dev"



###############################
def main():


	patList = "/data/projects/targetdbs/filtered-nt/downloads/nucl_*.accession2taxid.2017-05-21"
        fileList = glob.glob(patList)
	ntFile = "/data/projects/targetdbs/filtered-nt/downloads/nt.2017-05-21"

	FW = open("/data/projects/targetdbs/filtered-nt/generated/logfile.step1.txt", "w")
	ac2taxid = {}
	for fileName in fileList:
                if fileName.find("nucl_gb.accession2taxid") >= 0:
			i = 0
			with open(fileName, 'rb') as csvfile:
                		csvreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
                		for row in csvreader:
                        		seqAc = row[0].strip()
       					ac2taxid[seqAc] = 1
					if i%10000000 == 0:
						print "Done loading ", fileName, i
					i += 1
	

	i = 0
        for record in SeqIO.parse(ntFile, "fasta"):
                seqAc = record.id
		seqAc = seqAc.split('.')[0]
		if seqAc not in ac2taxid:
			FW.write("No taxid found for: %s\n" % (seqAc))
		if i%10000000 == 0:
			print "Done parsing",  i
		i += 1

	FW.close()


if __name__ == '__main__':
        main()

