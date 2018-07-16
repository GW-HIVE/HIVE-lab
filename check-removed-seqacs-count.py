import os,sys
import string
from optparse import OptionParser
from Bio import SeqIO
import glob
import MySQLdb
import csv
import util

__version__="1.0"
__status__ = "Dev"



####################################
def main():

	ac2taxidList1 = "/data/projects/targetdbs/filtered-nt/generated/logfile.ac2taxid.list.txt"
	ac2taxidList2 = "/data/projects/targetdbs/filtered-nt/generated/logfile.step3.manually.added.txt"
	blackListFile1 = "/data/projects/targetdbs/filtered-nt/generated/blacklist-taxId.unique.csv"
	FW = open("/data/projects/targetdbs/filtered-nt/generated/seqacs-removed.txt", "w")
	blackListClass = {}
	
	with open(blackListFile1, "rb") as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in csvreader:
			deter = True
			for key in blackListClass:
				if row[0] in blackListClass[key]:
					deter = False
			rmFactor = row[1].lower().split(';')[0]
			if deter:
				if rmFactor in blackListClass:
					blackListClass[rmFactor][row[0]] = set()
				else:
					blackListClass[rmFactor] = {}
					blackListClass[rmFactor][row[0]] = set()
	seqDup = {}

	with open(ac2taxidList1, 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in csvreader:
			seqAc = row[0].strip()
			taxId = row[1].strip()
			for key in blackListClass:
				if taxId in blackListClass[key]:
					blackListClass[key].setdefault(taxId, set()).add(seqAc)
			seqDup[seqAc] = seqDup.get(seqAc, 0) + 1

	blackListClass["unknown-manually"] = {}
				
	with open(ac2taxidList2, 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
		for row in csvreader:
			seqAc = row[0].strip()
			taxId = row[1].strip()
			for key in blackListClass:
				if taxId in blackListClass[key]:
					blackListClass[key].setdefault(taxId, set()).add(seqAc)
			if taxId == "NA":
				blackListClass["unknown-manually"].setdefault(taxId, set()).add(seqAc)
			seqDup[seqAc] = seqDup.get(seqAc, 0) + 1

	seqDupList = []
	seqDupDelete = 0
	seqDupAll = 0
	for key,val in seqDup.items():
		if val > 1:
			for a in blackListClass:
				for b in blackListClass[a]:
					if key in blackListClass[a][b]:
						seqDupDelete += 1
			seqDupAll += val - 1
			seqDupList.append([key,val])

	#for record in SeqIO.parse(ntFile, "fasta"):
	#	deter = True
         #       seqAc = record.id
          #      seqAc = seqAc.split('.')[0]
	for key in blackListClass:
		uniqueSeqAc = set()
		uniqueTaxId = set()
		for val in blackListClass[key]:
			if len(blackListClass[key][val]) != 0:
				uniqueTaxId.add(val)
				for i in blackListClass[key][val]:
					uniqueSeqAc.add(i)
		lenAcs = len(uniqueSeqAc)
		FW.write("%s,%s,%s\n" % (key, str(len(uniqueTaxId)), str(lenAcs)))

	FW.close()

	print len(seqDupList)
	print seqDupList
	print 'total duplicated seqacs', seqDupAll
	print 'duplicated seqacs in blacklist', seqDupDelete

if __name__ == '__main__':
        main()

