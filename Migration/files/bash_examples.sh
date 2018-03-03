#!/bin/bash
echo “MJ Setting up customized environment…”

df -h --output=source,used,avail,pcent



#! /bin/sh
#       this is my first shell script
#
echo "\n"
echo "Greetings! \c"
echo "Say, Gerhard - you are looking mighty sharp on this fine `date +%A`!\n"
echo "Just so you don't mix up your dates, today is `date +%D`\n"
echo "You are in directory `pwd` and you were most recently working on `ls -1Fc ~/ | head -1`.\n"
echo "Your shell is `echo $SHELL` and the available WiFi connection is `/home/gt/Scripts/./wifi.sh` \n"
echo "Your current file system looks like this: \n `df -k /home` \n"
echo "If you don't have the time to look out the window - here is the weather: \n `/home/gt/Scripts/./weather.sh 90049` \n"



echo "File system usage:"
echo "Filesystem\t      Size  Used Avail Use% Mount Point"
	df -h | egrep "^/dev"
echo
echo "Enter [q] to exit or [r] to refresh:\c"
read status
if [ $status = "q" ]
then
	exit 0
elif [ $status = "r" ]
then
	clear
fi