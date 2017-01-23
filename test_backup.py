#!/usr/bin/python
#encoding=utf-8
import MySQLdb
import sys
import logging
import os


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
                wordlist[3] = wordlist[3].strip('_')
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




def file_proc_logging( filename, cs, db ):
    try:
        f = open(filename)
    except IOError, e:
        logging.error("%s\n",e)
        return
    cnt = 0
    logging.info( "   %s %s %s\n", "="*60, filename, "="*30 )
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
                wordlist[3] = wordlist[3].strip('_')
                add_word = ( "INSERT INTO words(word,meaning,association,etyma) VALUES (%s, %s, %s, %s)" )
            else:  #something wrong
                logging.error( "wrong input format: %s", line )
                continue
            cs.execute( add_word, wordlist )
            cnt = cnt + 1
        except Exception, e:
            logging.error( "file_proc error at input file line :%serror: %s\n", line, e )
    db.commit()
    f.close()
    logging.info( "%s %s words inserted. %s\n", '-'*25, cnt, '-'*25 )



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
            wordstr = raw_input("\nENTER WORD:").strip()
            result = lookup_func(wordstr, cs) 
            if result != None:
                print result[0], '\t', result[1], '\t', result[2], '\t', result[3], '\t', result[4]
            else:
                print result
    except KeyboardInterrupt:
        print "\nLOOKUP FINISHED! exiting..."


def main():
    print "Welcome to Words BOOMING!"  
    try:
        logging.basicConfig(filename='log.log', level=logging.INFO, format='%(levelname)s %(asctime)s: %(message)s' )

        db = MySQLdb.connect( user='voila_words', passwd='', db='words_boom', charset='utf8' )  #host='127.0.0.1'
        cs = db.cursor()

        while True:
            mode = raw_input("\nEnter 1 to import words from files\nEnter 2 to look up mode\nEnter 3 to revise words\n").strip()
            if mode == '1':
                submode = raw_input("\nEnter 1 to import specific file\nEnter 2 to automatically import all the files under the specific directory\n").strip()
                if submode == "1":
                    files = raw_input("\nplease input vocabulary file names, seperated by TAB:\n").strip()
                    print
                    filelist = files.split('\t')
                    for filename in filelist:
                        file_proc(filename, cs, db)
                elif submode == "2":
                    dirs = raw_input("\ninput directory name to be traversed\n").strip()
                    for root,dirs,files in os.walk(dirs):
                        for f in files:
                            filename = os.path.join(root,f)
                            file_proc_logging(filename, cs, db)
            elif mode == '2':
                lookup_mode( cs )
            elif mode == "3":
                pass
    except KeyboardInterrupt:
        print "\nExiting..." 
    db.close()


if __name__=="__main__": main()
