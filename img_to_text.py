import sys
import os
from subprocess import call
import argparse
import requests
import io
import pytesseract
import time
import csv

VALID_IMAGES = [".jpg",".gif",".png",".tga",".tif",".bmp"]
FNULL = open(os.devnull, 'w')


class ArgumentMissingException(Exception):
    def __init__(self):
        print("usage: {} <dirname>".format(sys.argv[0]))
        sys.exit(1)
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def check_path(path):
    return bool(os.path.exists(path))

def main(input_path, output_path):
    if call(['which', 'tesseract']):
        print("tesseract-ocr missing, use sudo apt-get install tesseract-ocr to resolve")
    elif check_path(input_path):

        count = 0
        other_files = 0

        for f in os.listdir(input_path):
            ext = os.path.splitext(f)[1]

            if ext.lower() not in VALID_IMAGES:
                other_files += 1
                continue
            else :

                if count == 0:
                    create_directory(output_path)
                count += 1
                image_file_name = os.path.join(input_path, f)
                filename = os.path.splitext(f)[0]
                filename = ''.join(e for e in filename if e.isalnum() or e == '-')
                text_file_path = os.path.join(output_path, filename)
                call(["tesseract", image_file_name, text_file_path], stdout=FNULL)

                print(str(count) + (" file" if count == 1 else " files") + " completed")

        if count + other_files == 0:
            print("No files found at your given location")
        else :
            print(str(count) + " / " + str(count + other_files) + " files converted")
    else :
        print("No directory found at " + format(input_path))




def call_img(url):
    with open("ocr/testtext.txt",'w') as f:
        pass

    try:
        
        response = requests.get(url)
        file = open("sample_image.png", "wb")
        file.write(response.content)
        file.close()
        time.sleep(3)
        call(["tesseract", "sample_image.png", 'ocr/testtext'], stdout=FNULL)
        with open('ocr/testtext.txt') as f:
            contents = f.read()
            #print(contents)
        return contents        
    except:
        print("img is not downloaded")
        contents=''
        return contents




