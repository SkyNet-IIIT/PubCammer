# PubCammer

Python script to scrape images from the insecam video feeds, save locally, perform object detection and keep count of people in the images.

Downloading and installing dependancies through pip
```
pip3 install opencv-python beautifulsoup4 iso3166 imageai
```

The RetinaNet model file used in the script has to be downloaded via this [link](https://github.com/OlafenwaMoses/ImageAI/releases/download/essentials-v5/resnet50_coco_best_v2.1.0.h5/) and place in this same directory before running the script. 

Running the script for a specific cam and time interval
```
python3 pubcammer.py -o <cameraID> -f <folder_name> -t <time_interval>
```
