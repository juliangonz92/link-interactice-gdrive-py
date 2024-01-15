#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M")

# capture the image using cheese and save it to a file
fswebcam /home/juliangonzalez/Documentos/link-interactice-gdrive-py/$DATE.jpg

# return the image file path
echo "/home/juliangonzalez/Documentos/link-interactice-gdrive-py/$DATE.jpg"