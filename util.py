#!/usr/bin/env python
import re
import datetime
import os, hashlib, time, base64, string


def Authenticate(DBH, username, password, sessionId, maxSessionAge, auth):

	status, id, msg, fullname = 0, "", "", ""
	if username != '' and password != '':
		status, id, msg, fullname = TryLogin(DBH, username, password)
		if status == 1:
			status, id, fullname, msg = UpdateSession(DBH, username, 0, maxSessionAge)
	elif sessionId != '':
		status, sessionAge, msg = GetSessionAge(DBH, username, sessionId)
		if status == 1 and sessionAge < int(maxSessionAge):
			status, id, fullname, msg = UpdateSession(DBH, username, sessionAge, maxSessionAge)
		elif status == 0:
			fullname = ""
		else:
			msg = "Session timed out at " + str(sessionAge) + ' / ' +  maxSessionAge
			fullname = ""
			status = 0
	else:
		msg = "Not enough arguments"
	auth['status'], auth['id'], auth['fullname'], auth['msg'] = status, id, fullname, msg
	return


#~~~~~~~~~~~~~~~~~~~~~~~~~~~
def TryLogin(DBH, username, password):

	status, id, msg, fullname = 0, "", "", ""
	try:	
		cur = DBH.cursor()
		sql = ("SELECT passwd, fname, lname, sessionId, sessionTs FROM auth_user WHERE username = '%s' "
			% (username))
		cur.execute(sql)
		row = cur.fetchone()
		if row is None:
			msg = "Entered user name does not exist!"
		elif row[0] != password:
			msg = "Bad password!"
		else:
			msg = "Now logged in!"
			fullname = row[1] + ' ' + row[2]
			status = 1
	except:
		msg = "Login failed"

	return status, id, msg, fullname


#~~~~~~~~~~~~~~~~~~~~~~~~~~~
def UpdateSession(DBH, username, sessionAge, maxSessionAge):

	status, id, fullname, msg = 0, "", "", ""
	try:
		cur = DBH.cursor()
		id = MakeSessionId()  + MakeSessionId()
		string = "UPDATE %s set sessionId = '%s', sessionTs = CURRENT_TIMESTAMP "
		string += "WHERE username = '%s'"
		sql = (string % ("auth_user", id, username))
		cur.execute(sql)
		DBH.commit()
		msg = "Session updated at " + str(sessionAge) + "/" + str(maxSessionAge)
		status = 1
		sql = ("SELECT passwd, fname, lname, sessionId, sessionTs FROM auth_user WHERE username = '%s' "
                        % (username))
                cur.execute(sql)
                row = cur.fetchone()
                fullname = row[1] + ' ' + row[2]
	except:
		msg = "Update session failed"

        return status, id, fullname, msg




#~~~~~~~~~~~~~~~~~~~~~~~~~~~
def GetSessionAge(DBH, username, sessionId):

	status = 0
	msg = ''
	sql = ''
	sessionAge = 1000000
	try:
 		cur = DBH.cursor()
		string = "SELECT TIMESTAMPDIFF(SECOND, sessionTs, CURRENT_TIMESTAMP) sessionAge "
		string += " FROM %s WHERE  username = '%s' AND sessionId = '%s'"
		sql = (string % ("auth_user", username, sessionId))
		cur.execute(sql)
		row = cur.fetchone()
		sessionAge = row[0]
		status = 1
	except:
                status = 0
		msg = "GetSessionAge  failed"      
		   
	return status, sessionAge, msg




def EncryptString(password):
	m = hashlib.md5()
	m.update(password)
	return m.hexdigest()




def LoadParams(configfile, PHASH):

	FR = open(configfile, "r")
	lines = FR.readlines()
	for line in lines:
		if line[0] != "#" and len(line.strip()) > 0:
			param, value  = line.strip().split('|')
			if param in PHASH:
				PHASH[param] += value
			else:
			 	PHASH[param] = value
        FR.close()
	return


def LoadDivInfo(configfile, DHASH, pId):

        FR = open(configfile, "r")
        lines = FR.readlines()
        for line in lines:
                if line[0] != "#" and len(line.strip()) > 0:
                        pageid, divid, field, value  = line.strip().split('|')
                        if pageid == pId:
				if divid in DHASH:
                                	DHASH[divid] += (", \"%s\":\"%s\"" % (field, value))
                       	 	else:
                              		DHASH[divid] = ("\"%s\":\"%s\"" % ("id", divid))
					DHASH[divid] += (", \"%s\":\"%s\"" % (field, value))
        FR.close()
        return


def LoadGridInfo(configfile, DHASH, pId):

        FR = open(configfile, "r")
        lines = FR.readlines()
        for line in lines:
                if line[0] != "#" and len(line.strip()) > 0:
                        pageid, row, col, field, value  = line.strip().split('|')
                        cellid = str(row) + '_' + str(col)
			if pageid == pId:
                                if cellid in DHASH:
                                        DHASH[cellid] += (", \"%s\":\"%s\"" % (field, value))
                                else:
                                        DHASH[cellid] = ("\"%s\":\"%s\"" % ("id", cellid))
					DHASH[cellid] += (", \"%s\":\"%s\"" % ("row", row))
					DHASH[cellid] += (", \"%s\":\"%s\"" % ("col", col))
                                        DHASH[cellid] += (", \"%s\":\"%s\"" % (field, value))
        FR.close()
        return




#~~~~~~~~~~~~~~~~~~~~~
def  GetGlobalSections(PHASH):

	groups = PHASH['GSECTIONS'].split(';')
	tuples = ''
        for group in groups:
		sections = re.split(r'[:,]', group)
		label, secid, action, access = sections[1].split('^')
		tuples += '{"label":"'+label+'" , "id":"'+secid+'" , "action":"' + action + '"}';
		for i in range(2, len(sections)):
			label, secid, action, access = sections[i].split('^')
			tuples += ',{"label":"'+label+'" , "id":"'+secid+'" , "action":"' + action + '"}';
	return tuples;


#~~~~~~~~~~~~~~~~~~~~~
def  GetModuleSections(PHASH):

        groups = PHASH['SECTIONS'].split(';')
        tuples = ''
        for group in groups:
                sections = re.split(r'[:,]', group)
                label, secid, action, access = sections[1].split('^')
                tuples += '{"label":"'+label+'" , "id":"'+secid+'" , "action":"' + action + '"}';
                for i in range(2, len(sections)):
                        label, secid, action, access = sections[i].split('^')
                        tuples += ',{"label":"'+label+'" , "id":"'+secid+'" , "action":"' + action + '"}';
        return tuples;



def MakeSessionId():

	m = hashlib.md5()
	m.update(str(time.time()))
	m.update(str(os.urandom(64)))

	myStr = string.replace(base64.encodestring(m.digest())[:-3], '/', '$')
	return ''.join(e for e in myStr if e.isalnum())

