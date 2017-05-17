import sqlite3
import os
import time
import sys
import platform
import logging
import ctypes
import math
import os
import logging
import support

log = logging.getLogger(__name__)

con = sqlite3.connect('case.db')
cursor = con.cursor()

def opendb(case):
    global con
    global cursor
    if os.path.isfile('/Users/deb/Assignment03/case.db') and os.access("case.db", os.R_OK):
        con = sqlite3.connect("case.db")
        cursor = con.cursor() 
    else:
        con = sqlite3.connect(dbfilename) 
        cursor = con.cursor() 
        createNewTables(cursor)
        return cursor

def createNewTables(cursor):
    query = ''' 
    CREATE Table IF NOT EXISTS CASENAME (
    JPGName TEXT, ASCII TEXT, label TEXT, NSFW TEXT
    );
    ''' 
    cursor = con.cursor() 
    cursor.executescript(query) 
    return

def startCase(cursor,casename, Timestamp): 
    return (current)

def closedb(): 
    global con 
    con.commit() 
    con.close()

def insertinto(CASENAME, jpg, cursor, label, nsfw):
    #ASCII = "placeholder_for_ascii"
    #label = "placeholder_for_label"
    query = ('''INSERT INTO CASENAME (JPGName, label, nsfw) VALUES ("%s", "%s","%s")''' % (jpg, label, nsfw))
    cursor = con.cursor() 
    cursor.executescript(query)
    
if __name__ == '__main__': 
    CASENAME = 'TestCase' 
    cursor = opendb('case.db')
    createNewTables(cursor)
    closedb()

