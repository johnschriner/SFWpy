"""
========SFWpy======== 
input: url or image directory
output: categorized images and a NSFW evaluation and exports info to an SQLite database


SFWpy is very machine and environment-specific at the moment;
it relies on paths for one particular machine and it's terribly dependent on environmental packages 
(i.e. it won't work on your machine without massive configuration)

For directories: the script reads in the images
For URLs: the script scrapes the site using ImageScraper and reads in the images.

Images are first processed by Inception in Tensorflow, a neural network for categorizing images with good accuracy.
Then the images are processed through a Docker container supporting Caffe, the engine required for using Yahoo's open_nsfw evaluation.

Lastly, imagename/location as well as the categorization and NSFW evaluation are sent to an SQLite database

--To do:--
Flag images in db that score .7 or higher as NSFW for review
Add ability to change name of project
Work on interoperability -- may have to start over :/

Example usage and site:
python sfwpy.py -w psychic-vr-lab.com/deepdream/index_template.php?p=1  <-- does not work currently
python sfwpy.py -w www.imgur.com
python sfwpy.py -d images
python sfwpy.py -w boards.4chan.org/b  <--nope

"""

import os, sys, time, glob
import classify_image
import support_sql
import time
import argparse
import sys
import subprocess as sub
from collections import deque

def ParseCmdLine(DESCRIPTION="SFWpy"): #this parser gives us an easy solution for command line help and arguments, called first.
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-w','--webpage', required=False, action='store',help='Please provide a website to scrape the images from e.g. -w www.imgur.com')  #what name to prefix the logs
    parser.add_argument('-d','--directory', required=False, action='store', help='Please provide a directory of images e.g. -d images/')
    global gl_args #gl_args is now known globally: i.e. outside of this function
    #gl_args = parser.parse_args()
    gl_args = parser.parse_args()
    
def getpics():
    if gl_args.webpage:
        os.system("image-scraper " + gl_args.webpage + " --formats gif jpg jpeg")
        global wd
        wd = str('images_' + gl_args.webpage)
        print wd
        return wd
    if gl_args.directory:
        wd = str(gl_args.directory)
        return wd
    else:  #work on this
        return "Please provide either a website or a directory of images to process"


def tail(filename, n=5):
    return deque(open(filename), n)

def grabascii():            #silly, but fun
    f = open("asciiexport.txt","r")
    grabbed = f.readlines()
    print str(grabbed)
    
def grablabel():
    f = open("tensorexport.txt","r")
    grabbed = f.read().replace('\n', '')
    global label
    label = str(grabbed)
    return label

def filefordocker(filename):
    f = open('filefordocker.txt','w')
    f.write(filename)
    f.close

def grabnsfw():
    grabbed = file("nsfwexport.txt","r").readlines()[-1]
    #grabbed = f.read().replace('\n', '')
    global nsfw
    nsfw = str(grabbed)
    print nsfw
    return nsfw

def classify():
    #wd = "images/"   #default random photos
    #wd = "images/good_for_ascii/" #directory with un-trained photos from deepdream
    CASENAME = "TestCasename"
    print wd
    justjpgs =  glob.glob(wd + '/*.jpg')    
    for jpg in justjpgs:
        print ("Processing the image: " + jpg)
        filefordocker(jpg)
        asciiimg = os.system("jp2a "+ jpg + " > asciiexport.txt") #type = int
        os.system("python /Users/deb/git/models/tutorials/image/imagenet/classify_image.py --num_top_predictions 3 --image_file " + jpg + " > tensorexport.txt")  #returns a zero if assigned a variable
        #os.system("python classify_image.py --num_top_predictions 3 --model_dir '/Users/deb/Downloads/tf_retrained/' --image_file " + jpg + " > tensorexport.txt")  #returns a zero if assigned a variable so I can grab it from an exported txt
        cursor = support_sql.opendb('case.db')
        support_sql.createNewTables(cursor)
        ASCII = "placeholder_for_ascii"
        grablabel()
        time.sleep(2)
        print jpg
        #os.system("docker run -it -p 8888:8888 -p 6006:6006 -v /Users/deb/Documents/FCM790/Assignment03/:/root/sharedfolder floydhub/dl-docker:cpu -c 'python sharedfolder/open_nsfw/classify_nsfw.py \
            #--model_def sharedfolder/open_nsfw/nsfw_model/deploy.prototxt \
            #--pretrained_model sharedfolder/open_nsfw/nsfw_model/resnet_50_1by2_nsfw.caffemodel \
            #sharedfolder/open_nsfw/nonporn/orig.jpg' > nsfwexport.txt") #opens docker container, performs nsfw check, and writes to file 
        #os.system("docker run -it -p 8888:8888 -p 6006:6006 -v /Users/deb/Documents/FCM790/Assignment03/:/root/sharedfolder floydhub/dl-docker:cpu bash -c 'a=(cat /sharedfolder/filefordocker.txt) && python sharedfolder/open_nsfw/classify_nsfw.py \
            #--model_def sharedfolder/open_nsfw/nsfw_model/deploy.prototxt \
            #--pretrained_model sharedfolder/open_nsfw/nsfw_model/resnet_50_1by2_nsfw.caffemodel sharedfolder/$a' > sharedfolder/nsfwexport.txt") #opens docker container, performs nsfw check, and writes to file          
        os.system("docker run -it -p 8888:8888 -p 6006:6006 -v /Users/deb/Documents/FCM790/Assignment03/:/root/sharedfolder floydhub/dl-docker:cpu bash -c 'A=`cat sharedfolder/filefordocker.txt` && python sharedfolder/open_nsfw/classify_nsfw.py --model_def sharedfolder/open_nsfw/nsfw_model/deploy.prototxt --pretrained_model sharedfolder/open_nsfw/nsfw_model/resnet_50_1by2_nsfw.caffemodel sharedfolder/$A' > nsfwexport.txt")
        os.system("docker stop $(docker ps -a -q)")        
        time.sleep(2)
        grabnsfw()
        support_sql.insertinto(CASENAME, jpg, cursor, label, nsfw)
        print "----------------"
        support_sql.closedb()        
     
if __name__ == '__main__':
    ParseCmdLine()
    getpics()    
    classify()


