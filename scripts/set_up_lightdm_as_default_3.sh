#!/bin/bash

# Set up lightdm as display window manager
sudo cat "/usr/sbin/lightdm" | sudo tee /etc/X11/default-display-manager > /dev/null
