#!/usr/bin/python3
from urllib import request # request for targz file
import tarfile # open tar file
import io # bytesIO object
import sys # error handling
import os
import argparse # parse arguments
from argparse import RawTextHelpFormatter #change parser display


def main():
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('-boot', type=str,
                        default='https://github.com/apollo-lhc/SM_ZYNQ_FW/releases/',
                        help='source for BOOT.BIN, can be url (start with https://) or local directory (start with / or ./)\ndefault: https://github.com/apollo-lhc/SM_ZYNQ_FW/releases/')
    parser.add_argument('-image', type=str,
                        default='https://github.com/apollo-lhc/SM_ZYNQ_FW/releases/',
                        help='source for image.ub, can be url (start with https://) or local directory (start with / or ./)\ndefault: https://github.com/apollo-lhc/SM_ZYNQ_FW/releases/')
    parser.add_argument('-tar', type=str,
                        default='https://github.com/apollo-lhc/SM_ZYNQ_FW/releases/',
                        help='source for SD_p2.tar.gz, can be url (start with https://) or local directory (start with / or ./)\ndefault: https://github.com/apollo-lhc/SM_ZYNQ_FW/releases/')
    parser.add_argument('-ver', type=str, 
                        default='1.4.2',
                        help='version of BOOT.BIN, image.ub, and SD_p2.tar.gz, ignored when source is local directory\ndefault: 1.4.2')
    parser.add_argument('-zynq', type=str, 
                        default='',
                        help='zynq version of BOOT.BIN and image.ub, ignored when source is local directory\ndefault is empty')
    parser.add_argument('-dir', type=str, 
                        default='./',
                        help='directory which the files will be written to\ntar.gz files will be written to DIR, BOOT.BIN and image.ub will be written to DIR/fw\ndefault DIR: ./')

    args = parser.parse_args()

    try:
        getFiles(args)
        writeFiles(args.dir)
    except Exception as error:
        print(error.args)

def isWeb(x):
    return (x.startswith('https://') or x.startswith('http://'))

def getFiles(args):
    bootSource = args.boot.strip()
    imageSource = args.image.strip()
    tarSource = args.tar.strip()
    version = 'v' + args.ver.strip()
    zynq = args.zynq.strip()

    if zynq:
        zynq = '.' + zynq

    global bootF
    try: 
        if (isWeb(bootSource)):
            bootUrl = bootSource+'download/'+version+'/BOOT.BIN'+zynq
            print("Downloading BOOT.BIN from", bootUrl)
            res = request.urlopen(bootUrl)
            with res as r:
                bootF = io.BytesIO(r.read())
        else:
            print("Loading BOOT.BIN from", bootSource)
            with open(bootSource, mode='rb') as boot:
                bootF = io.BytesIO(boot.read())
    except:
        raise Exception('Invalid BOOT.BIN source')

    global imageF
    try:
        if (isWeb(imageSource)):
            imageUrl = imageSource+'download/'+version+'/image.ub'+zynq
            print("Downloading image.ub from", imageUrl)
            res = request.urlopen(imageUrl)
            with res as r:
                imageF = io.BytesIO(r.read())
        else:
            print("Loading image.ub from", imageSource)
            with open(imageSource, mode='rb') as image:
                imageF = io.BytesIO(image.read())
    except:
        raise Exception('Invalid image.ub source')

    global tarF
    try:
        if (isWeb(tarSource)):
            tarUrl = tarSource+'download/'+version+'/SD_p2.tar.gz'+zynq
            print("Downloading SD_p2.tar.gz from", tarUrl)
            res = request.urlopen(tarUrl)
            with res as r:
                tarF = io.BytesIO(r.read())
        else:
            print("Loading SD_p2.tar.gz from", tarSource)
            with open(tarSource, mode='rb') as tar:
                tarF = io.BytesIO(tar.read())
    except:
        raise Exception('Invalid SD_p2.tar.gz source')

def writeFiles(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

    dirFw = dir + 'fw/'
    if not os.path.exists(dirFw):
        os.makedirs(dirFw)

    print('Writing BOOT.BIN to ', dirFw + 'BOOT.BIN')
    with open(dirFw + 'BOOT.BIN', 'wb') as boot:
        boot.write(bootF.read())

    print('Writing image.ub to ', dirFw + 'image.ub')
    with open(dirFw + 'image.ub', 'wb') as image:
        image.write(imageF.read())

    print('Extracting SD_p2.tar.gz to ', dirFw)
    tar = tarfile.open(fileobj=tarF, mode='r:gz')
    tar.extractall(dir, numeric_owner=True)

if __name__ == '__main__':
    main()