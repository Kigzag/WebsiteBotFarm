# WebsiteBotFarm
WebsiteBotFarm

Refer to https://gist.github.com/bvolpato/9724ad2b0c90d78429c7223d52258dea
on how to setup xvfb for ec2 to run headfull chrome browser for google analytics to detect users

#!/bin/bash

# Chrome Repo
sudo apt-get install fonts-liberation xdg-utils libxss1 libappindicator1 libindicator7
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome*.deb

sudo apt-get update

# Download
wget https://chromedriver.storage.googleapis.com/2.22/chromedriver_linux64.zip

#Extract
unzip chromedriver_linux64.zip

# Deploy + Permissions
sudo cp ./chromedriver /usr/bin/
sudo chmod ugo+rx /usr/bin/chromedriver

# Install Google Chrome:
sudo apt-get -y install libxpm4 libxrender1 libgtk2.0-0 libnss3 libgconf-2-4

# Dependencies to make "headless" chrome/selenium work:
sudo apt-get -y install xorg xvfb gtk2-engines-pixbuf
sudo apt-get -y install dbus-x11 xfonts-base xfonts-100dpi xfonts-75dpi xfonts-cyrillic xfonts-scalable

# Optional but nifty: For capturing screenshots of Xvfb display:
sudo apt-get -y install imagemagick x11-apps

# Make sure that Xvfb starts everytime the box/vm is booted:
echo "Starting X virtual framebuffer (Xvfb) in background..."
Xvfb -ac :99 -screen 0 1280x1024x16 &
export DISPLAY=:99


# Optionally, capture screenshots using the command:
#xwd -root -display :99 | convert xwd:- screenshot.png
