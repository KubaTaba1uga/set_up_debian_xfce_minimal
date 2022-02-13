#!/bin/bash

non_interactive="DEBIAN_FRONTEND=noninteractive"

# Install X windows server
sudo  $non_interactive apt-get install -y --no-install-recommends  \
	xserver-xorg \
	xfonts-base xinit \
	xserver-xorg-core

