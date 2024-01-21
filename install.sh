#! /usr/bin/env bash


#UNCOMMENT if you run into a permission error when installing this module on ubuntu.

# if ! command -v virtualenv &> /dev/null; then
#     sudo apt install virtualenv
# fi 

# virtualenv . 
# source ./bin/activate

# add "--user" to this if you don't have access to your computer's system-wide python packages.

pip3 install --editable .