# PubCammer

Python script to scrape images from the insecam video feeds, save locally, perform object detection and keep count of people in the images.

Downloading and installing dependancies through pip
```
pip3 install opencv-python beautifulsoup4 iso3166 imageai
```

Running the script for a specific cam and time interval
```
python3 pubcammer.py -o <cameraID> -f <folder_name> -t <time_interval>
```
