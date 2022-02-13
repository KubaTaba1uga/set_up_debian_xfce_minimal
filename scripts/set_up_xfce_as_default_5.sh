#!/bin/bash

sed '/\[Seat\:\*\]/a user-session=xfce' /etc/lightdm/lightdm.conf | sudo tee /etc/lightdm/lightdm.conf > /dev/null
