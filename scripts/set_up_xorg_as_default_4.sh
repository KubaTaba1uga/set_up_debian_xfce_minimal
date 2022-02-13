#!/bin/bash

sed '/\[Seat\:\*\]/a xserver-backend=xorg' /etc/lightdm/lightdm.conf | sudo tee /etc/lightdm/lightdm.conf > /dev/null


sed '/\[Seat\:\*\]/a xserver-command=Xorg' /etc/lightdm/lightdm.conf | sudo tee /etc/lightdm/lightdm.conf > /dev/null
