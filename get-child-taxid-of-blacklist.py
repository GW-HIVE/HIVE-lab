#!/usr/bin/python
import os,sys
import string
import cgi
import commands
from optparse import OptionParser
import json
import util
import MySQLdb
import csv


__version__="1.0"
__status__ = "Dev"


###################################
def getLineage(taxId, className):

        cur1 = DBH.cursor()
        lineage = []
        string = "SELECT A.taxId, B.nameTxt FROM NCBI_node A, NCBI_name B "
        string += "WHERE A.taxId = B.taxId AND A.parentTaxId = %s "
        sql = (string % (taxId))
        cur1.execute(sql)
        for row in cur1.fetchall():
                childTaxId = row[0]
                taxName = row[1]
                print str(childTaxId) + ',' + className + ',' + taxName
                if childTaxId != 1:
                        getLineage(childTaxId, className)
        return




####################################
def main():

	taxIdFile = "/data/projects/targetdbs/filtered-nt/generated/blacklist-taxId.1.csv"

        global PHASH
        global AUTH
        global DBH
	
	PHASH = {}

	util.LoadParams("/projects/gfkb/cgi-bin/conf/database.txt", PHASH)
	DBH = MySQLdb.connect(host = PHASH['DBHOST'], user = PHASH['DBUSERID'],
                        passwd = PHASH['DBPASSWORD'], db = PHASH['DBNAME'])

	with open(taxIdFile, 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in csvreader:
			taxId = row[0]
			className = row[1]
			print taxId + ',' + row[1] + ',' + row[2]
			lineage = getLineage(taxId, className)
	DBH.close()


if __name__ == '__main__':
        main()

