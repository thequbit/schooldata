import sys
import re
import csv
import sqlite3

def readfile(infile):
    contents = []
    with open(infile,'r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        if not line == '':
            contents.append(line)
    return contents

def parselines(contents):
    schools = []
    rank = 1
    for line in contents:
        school = line.split('(')[0].split('.')[1].strip()
        county = line.split('(')[1].split(',')[0].strip()
        #print "School: {0} - {1}".format(school, county)
        schools.append((rank,school,county))
        rank += 1
    return schools

def createdb(schools,outfile):
    con = sqlite3.connect(outfile)
    cur = con.cursor()

    query = """CREATE TABLE schools
               (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   rank INTEGER,
                   name TEXT,
                   county TEXT
               )
            """
    cur.execute(query)

    for school in schools:
        rank,name,county = school
        #query = 'INSERT INTO schools(rank,name,county) VALUES(?,?,?)'
        #print query
        cur.execute("INSERT INTO schools(rank,name,county) VALUES(?,?,?)",(rank,name,county))
        print "Added {0}: {1}, {2}, {3}".format(cur.lastrowid, rank, name, county)

    cur.close()
    con.close()

def main(argv):

    if len(argv) != 3:
        print "\nUsage:\n\tpython {0} <rawfile.txt> <output.sqlite> \n\n".format(argv[0])
        return

    infile = argv[1]
    outfile = argv[2]

    contents = readfile(infile)
    schools = parselines(contents)
    createdb(schools,outfile)

if __name__ == '__main__': sys.exit(main(sys.argv))