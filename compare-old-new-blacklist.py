import os,sys
import string
from optparse import OptionParser
from Bio import Entrez, SeqIO
import glob
import MySQLdb

__version__="1.0"
__status__ = "Dev"



###############################
def main():


	newFile = "/data/projects/targetdbs/filtered-nt/generated/blacklist-taxId.unique.csv"
	oldFile = "/data/projects/targetdbs/filtered-nt/generated/Blacklist_version1_all_taxID_YH.txt"
	compareFile = "/data/projects/targetdbs/filtered-nt/generated/compare-new-old-blacklist.txt"

	oldList = {}
	FR1 = open(oldFile, "r")
	FR2 = open(newFile, "r")
	FW = open(compareFile, "w")
	for line in FR1:
		line = line.strip().split('\t')
		try:
			oldList[line[0]] = line[1]
		except:
			oldList[line[0]] = "NA"
	FR1.close()

	newList = {}
	i = 0
	for line in FR2:
		line = line.strip().split(',')
		if not line[0] in oldList:
			FW.write("Newly added taxIds: %s,%s\n" % (line[0],line[1]))
		else:
			i += 1
		newList[line[0]] = 1
	FR2.close()

	for j in oldList:
		if not j in newList:
			FW.write("Deleted taxIds: %s,%s\n" % (j,oldList[j]))
	FW.close()
	print "The number of taxIds included in both old and new black list is:",i

if __name__ == '__main__':
        main()

