#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M")

# capture the image
image_data=$(fswebcam -r 1280x720 --no-banner /home/pi/$DATE.jpg)

# return the image data
echo $image_data
