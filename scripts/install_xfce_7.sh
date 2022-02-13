#!/bin/bash

non_interactive="DEBIAN_FRONTEND=noninteractive"

# Install GUI
sudo  $non_interactive apt-get install -y --no-install-recommends \
    libxfce4ui-utils \
    thunar \
    xfce4-appfinder \
    xfce4-panel \
    xfce4-pulseaudio-plugin \
    xfce4-whiskermenu-plugin \
    xfce4-session \
    xfce4-settings \
    terminator \
    xfconf \
    xfdesktop4 \
    xfwm4 \
    adwaita-qt \
    qt5ct 
