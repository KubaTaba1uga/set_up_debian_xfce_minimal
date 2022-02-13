#!/bin/bash

apt-get install sudo -y  --no-install-recommends

loop_controll=true

while $loop_controll
do
	echo $'\n'Which user should be add to sudoers?
	read user
	# If user added to group, disable password requirement
	usermod -a -G sudo $user && echo "$user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

	echo $'\n'Sudo group summary$'\n'
	getent group | grep sudo 

	echo $'\n'"Add another user?[y/n]"
	read quit

	if [ $quit == n ]
	then 
		loop_controll=false
	fi
done
