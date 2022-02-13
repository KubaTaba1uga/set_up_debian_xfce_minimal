#!/bin/bash

non_interactive="DEBIAN_FRONTEND=noninteractive"

# Install display manager
sudo  $non_interactive apt-get install lightdm -y  --no-install-recommends

# Start lightdm 
sudo systemctl start lightdm
# Start lightdm on starttup
sudo systemctl enable lightdm

