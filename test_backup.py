#!/usr/bin/python
#encoding=utf-8
import MySQLdb
import sys

def file_proc( filename, cs, db ):
    try:
        f = open(filename)
    except IOError, e:
        print e, "\n"
        return
    cnt = 0
    print "="*60, '\n', filename, "\n", "-"*15, '\n'
    for line in f:
        try:
            lineplus = line.strip(' \n')
            wordlist = lineplus.split('\t\t')
            num = len(wordlist)
            if num == 1 :   # no chinese meaning
                add_word = ( "INSERT INTO words(word) VALUES (%s)" )
            elif num == 2 :  # chinese meaning
                add_word = ( "INSERT INTO words(word,meaning) VALUES (%s, %s)" )
            elif num == 3 :  # chinese meaning and etyma/association
                if wordlist[2].startswith('__') :  #etyma
                    wordlist[2] = wordlist[2].lstrip('_')
                    add_word = ( "INSERT INTO words(word,meaning,etyma) VALUES (%s, %s, %s)" )
                else:                             #association
                    add_word = ( "INSERT INTO words(word,meaning,association) VALUES (%s, %s, %s)" )
            elif num == 4 :  # chinese meaning and association and etyma
                add_word = ( "INSERT INTO words(word,meaning,association,etyma) VALUES (%s, %s, %s, %s)" )
            else:  #something wrong
                print "wrong input format: "+line
                continue
            cs.execute( add_word, wordlist )
            cnt = cnt + 1
        except Exception, e:
            print "file_proc error at input file line :", line, " error: ", e, "\n"
    db.commit()
    f.close()
    print "-"*15,'\n', cnt, " words inserted.\n"


def lookup_func( wordstr, cs ):
    try:
        cs.execute( "SELECT * FROM words WHERE word = %s", wordstr )
        result = cs.fetchone()
        return result
    except Exception, e:
        print "Something wrong: ", e


def lookup_mode( cs ):
    try:
        while True:
            wordstr = raw_input("\nENTER WORD:")
            result = lookup_func(wordstr, cs) 
            if result != None:
                #print ', '.join( str(result) )
                print result[0], '\t', result[1], '\t', result[2], '\t', result[3], '\t', result[4]
            else:
                print result
    except KeyboardInterrupt:
        print "\nLOOKUP FINISHED! exiting..."


###########################################################################
print "Welcome to Words BOOMING!"  
try:
    db = MySQLdb.connect( user='voila_words', passwd='', db='words_boom', charset='utf8' )  #host='127.0.0.1'
    cs = db.cursor()
    while True:
        mode = raw_input("\nEnter 1 to import words from file\nEnter 2 to look up mode\n")
        if mode == '1':
            files = raw_input("\nplease input vocabulary file names, seperated by TAB:\n")
            print
            filelist = files.split('\t')
            for filename in filelist:
                file_proc(filename, cs, db)
        elif mode == '2':
            lookup_mode( cs )
except KeyboardInterrupt:
    print "\nExiting..." 

db.close()
