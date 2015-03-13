#!/usr/bin/env python2.7
#
# PodcastXDL.py - A Simple Podcast client for the Terminal.
#
# See LICENSE file.
#
# -*- coding: utf-8 -*-

import sys
import urllib2
import getopt
from time import sleep
import os
from socket import * 

try:
    import feedparser

except ImportError:
    print "\033[01;31m[PodCastXDL] Error: feedparser not found!\033[00m"
    print "\033[01;01m\nInstall:"
    print "\tDebian/Ubuntu: sudo apt-get install python-feedpaser"
    print "\tArchlinux: sudo pacman -S python2-feedparser"
    print "\tFedora: sudo yum install python-feedparser"
    print "\n\tfor another OS: https://pypi.python.org/pypi/feedparser\n"
    sys.exit(1)


__author__ = "levi0x0"
__version__ = "0.8"
__date__ = "28/02/2013"
__license__ = "GPL 3"

logo = "Starting PodcastXDL %s - Copyright (c) 2014,2015 by levi0x0" % (__version__)

DEBUG = False
USER_AGENT = "M"

# Defualt Block size
DEFAULT_BLOCK_SIZE = 9192

# XXX: DONT MODIFY!
quiet = False
links = False
folder = "./"
dl_format = "mp3"
startp = 1
title = False
number = False
history = False
stopat = -1
restore = False

class PodCastXDL(object):
        def __init__(self, feed, folder, dl_format, startp, title, number, history,stopat):

            self.feed_url = feed
            self.folder = folder
            self.links = []
            self.dl_format = dl_format
            self.startp = startp
            self.podcast_counter = 0
            self.title = title
            self.number = number
            self.history = history
            self.podtitle = []
            """
                You must use a vaild .config folder for PodCastXDL
            """
            self.config_folder = "%s/.config/" %(os.path.expanduser('~'))
            self.config_folder_path = "%s/PodCastXDL/" % self.config_folder
            self.stopat = stopat
            self.feeds = []

        def parse_feed(self):

            self.feed = feedparser.parse(self.feed_url)            
            if not quiet:
                print "\033[H\033[J"
                print "\033[01;32m%s\033[00m\n" % logo 
                print "[*] Fetching: %s..." % self.feed_url

            for i in self.feed.entries:
                for link in i.links:
                    if link['href'].endswith(self.dl_format):
                        self.podcast_counter += 1
                        self.links.append(link['href'])
                    else:
                        pass
            if self.title:
                for x in self.feed.entries:
                        self.podtitle.append(x.title.replace(" ", "_"))

            if not quiet:
                print "[+] Success! Found: %d - %s Files." %(self.podcast_counter,
                        self.dl_format) 
                #do not remove this delay
                sleep(2)
        
        def dump_links(self):
            for dlink in self.links:
                print dlink
            sys.exit(0)

	def convert_bytes(self, bytes):
		bytes = float(bytes)
   	        smb = 1024 * 1024 	
                if bytes >= smb:
        		mb = bytes / smb
        		size = '%.2fM' % mb
    		elif bytes >= 1024:
        		k = bytes / 1024
        		size = '%.2fK' % k
    		else:
        		size = '%.2fb' % bytes

    		return size

        def check_internet(self):
            pass
        def parse_config(self, line):
            i = 0
            self.config_path = "%s/Config" % (self.folder)
            if os.path.exists(self.config_path):
                conf = open(self.config_path, "rt").readlines()
                for li in conf:
                    i += 1
                    if i == line:
                        return int(li)
                        pass
            else:
                return False

        def feeds_history(self, opt):
            feeds_history_path = "%s/feeds_history" % self.config_folder_path

            if opt == "read":
                read = open(feeds_history_path, "rt").readlines()
                for feed in read:
                    feed = feed.replace("\n", "")
                    self.feeds.append(feed)
                return self.feeds

            elif opt == "write":
                conf = open(feeds_history_path, "a+")
                conf.write("%s\n%s\n" % (self.feed_url, self.folder))
                conf.close()
        
        def write_config(self, arg):
            conf = open(self.config_path, "wt")
            conf.write(str(arg))
            conf.close()
            
        def checks(self):
            if not os.path.exists(self.folder):
                os.mkdir(self.folder)
            else:
                pass
            
            if not os.path.exists(self.config_folder_path):
                os.mkdir(self.config_folder_path)
            if not os.path.exists(self.config_folder):
                os.mkdir(self.config_folder)

            else:
                pass
            os.chdir(self.folder)

        def sync(self):
            local_podcasts = self.parse_config(2)
            remote_podcasts = self.podcast_counter

            if remote_podcasts > local_podcasts:
                print "There is: %s New Files." % ( remote_podcasts - local_podcasts)
            else:
                if remote_podcasts == local_podcasts:
                    print "All the files has been downloaded.."
                    exit(1)
        def download_files(self):
            global file_name
            
            self.sync()
            self.checks()
            self.feeds_history("write")
            counter = 0

            if not self.parse_config(2):
                pass
            else:
                self.startp = int(self.parse_config(2))

            for link in self.links:
                if not quiet:
                    print "\033[H\033[J"
                    print "\033[01;01m%s\033[00m\n" % logo
                counter += 1
               
                self.write_config("%d\n%d" % (self.podcast_counter, counter))

                if counter == self.stopat + 1:
                    print "[+] Done!"
                    break
                if counter >= self.startp:
                    if not self.title:
                        file_name = link.split("/")[-1]
                    elif self.title:
                        title = self.podtitle[counter-1]
                        file_name = "%s.%s" % (title, self.dl_format)
                    if not self.number:
                        pass
                    elif self.number:
                        file_name = "%d.%s" % (counter, self.dl_format)

                    if self.title:
                        sys.stdout.write("\n\033[01;34mDownloading %s: %d/%d... \033[00m" %(title, counter, 
                                self.podcast_counter))
                    else: 
                        sys.stdout.write("\n\033[01;34mDownloading file %d/%d... \033[00m" %(counter,
                             self.podcast_counter))
                    opener = urllib2.build_opener()
                    opener.addheaders = [('User-Agent', USER_AGENT)]
                    u = opener.open(link)
		    f = open(file_name, 'wb')
		    meta = u.info()
		    file_size = int(meta.getheaders("Content-Length")[0])

		    file_size_dl = 0
		    block_sz = DEFAULT_BLOCK_SIZE
		    while True:
   		        buffer = u.read(block_sz)
    		        if not buffer:
        		    break

    		        file_size_dl += len(buffer)
    		        f.write(buffer)
    		        status = r"%10s/%s (%3.2f%%)" % (self.convert_bytes(file_size_dl),
                                self.convert_bytes(file_size),
				file_size_dl * 100. / file_size)
    		        status = status + chr(8)*(len(status)+1)
    		        print status,

		    f.close()           

                else:
                    pass

def print_usage():
    print "\033[01;01m"
    print "PodCastXDL %s - Copyright (c) 2014,2015 by levi0x0\n" % __version__
    print "Usage: ./PodCastXDL.py [OPTIONS].."
    print "\n\tOptions:"
    print "\t\t-u, --url - feed url."
    print "\t\t-d, --dir - download folder."
    print "\t\t-f, --format - Ffeed download format. (Default: mp3)"
    print "\t\t-v, --version - print version and exit."
    print "\t\t-l, --links - do not download, print only links."
    print "\t\t-q, --quiet - do not print output."
    print "\t\t-t, --title - Rename podcast file to podcast title."
    print "\t\t-n, --number - Rename file name to number order by files.."
    print "\t\t-H, --history - read feeds History."
    print "\t\t-s, --start-from - start download from specific podcast number."
    print "\t\t-a, --stop-at - stop download at specific  number."
    print "\t\t-r, --restore - restore previous  download."
    print "\t\t-h, --help - print help."
    print "\n\tUsage Example:"
    print "\t\t./PodCastXDL.py -u http://foo.foo/feed -d ~/Downloads/\n"

def main():
    try:
        start = PodCastXDL(feed, folder, dl_format, startp, title, number, history,stopat)
        start.check_internet()
        start.parse_feed()
        if links:
            start.dump_links()
        elif history:
            for i in start.feeds_history("read"):
                    print "%s" % i
            sys.exit(1)
        else:
            start.download_files() 
    except KeyboardInterrupt:
        print "\n\033[01;32mInterrupt ):\033[00m"
        os.remove(file_name)
        sys.exit(1)

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "vu:f:d:s:lqtnHa:r")
    except getopt.GetoptError as err: 
            print "\033[01;31m%s\033[00m\n" % err
            print_usage()
            sys.exit(1)
    except ValueError:
        print_usage()
        sys.exit(1)

    for o, a in opts:
        if o in  ("-v", "--version"):
            print __version__ 
            sys.exit(0)
        elif o in ("-u", "--url"):
            if not "://" in a:
                print "[ERROR] %s - bad link." % a
                sys.exit(1)
            else:
                feed = a
        elif o in ("-f", "--format"):
            dl_format = a
        elif o in ("-d", "--dir"):
            folder = a
        elif o in ("-l", "--links"):
            links = True
            quiet = True
        elif o in ("-t", "--title"):
            title = True
        elif o in ("-q", "--quiet"):
            quiet = True
        elif o in ("-H", "--history"):
            feed = ""
            quiet = True
            history = True
        elif o in ("-n", "--number"):
            number = True
        elif o in ("-a", "--stop-at"):
            stopat = int(a)
        elif o in ("-h", "--help"):
            print_usage()
            sys.exit()
        elif o in ("-s", "--start-from"):
            startp = int(a)
        elif o in ("-r", "--restore"):
            restore = True
            try:
                # Mac users change this
                seek_feed = open("%s/.config/PodCastXDL/feeds_history" % os.path.expanduser('~'), "r").readlines()[-2]
                seek_folder = open("%s/.config/PodCastXDL/feeds_history" % os.path.expanduser('~'), "r").readlines()[-1]
            except IOError:
                print "[!] feeds_history file Not exists!"
                exit()
            feed = seek_feed.replace('\n', '')
            folder = seek_folder.replace('\n', '')

    try:

        main()

    except NameError as e:
        if DEBUG:
            print e.message
        print_usage()
        sys.exit()

    except error as e:
        print "\n\033[01;31m[ERROR] %s\033[00m" % e.message
        sys.exit(1)
    except IOError as e:
        print "\033[01;31m%s\033[00m" % e.message
        sys.exit(1)
