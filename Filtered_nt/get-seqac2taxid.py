import os,sys
import string
from optparse import OptionParser
from Bio import SeqIO
import glob
import csv


__version__="1.0"
__status__ = "Dev"



###############################
def main():


	patList = "/data/projects/targetdbs/downloads/ac2taxid.2017-05-30/*"
        fileList = glob.glob(patList)
	ntFile = "/data/projects/targetdbs/downloads/nt.2017-05-21"
	manualFile = '/data/projects/targetdbs/generated/logfile.step3.manually.added.txt'
	FW = open("/data/projects/targetdbs/generated/logfile.ac2taxid.list.txt", "w")

	ac2taxid = {}
	for record in SeqIO.parse(ntFile, "fasta"):
		seqAc = record.id
		seqAc = seqAc.split('.')[0].upper()
		ac2taxid[seqAc] = 1
	print "Data loading done"

	manual = open(manualFile, "r")
	for row in manual:
		row = row.strip().split('\t')
		if row[0] in ac2taxid:
			FW.write(row[0] + ',' + row[1] + '\n')
	manual.close()

	for fileName in fileList:
		i = 0
		with open(fileName, 'rb') as csvfile:
                	csvreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
                	for row in csvreader:
                       		seqAc = row[0].strip().upper()
				if seqAc in ac2taxid:
					FW.write(seqAc + ',' + row[2].strip() + '\n')
				if seqAc+seqAc[-1] in ac2taxid and fileName.find('pdb.accession2taxid') >= 0:
					FW.write(seqAc+seqAc[-1] + ',' + row[2].strip() + '\n')
				if i%10000000 == 0:
					print "Done loading ", fileName, i
				i += 1
	FW.close()


if __name__ == '__main__':
        main()

