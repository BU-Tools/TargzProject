#!/usr/bin/python3
import tarfile  # open tar file
import io  # bytesIO object
import sys  # error handling
import os  # path join
import argparse  # parse arguments
from argparse import RawTextHelpFormatter  # change parser display
from tqdm import tqdm  # progress bar
import requests  # http request


def main():
    # check root privilege
    if os.geteuid() != 0:
        exit("You need to have root privileges to run this script.")

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


# chech whether the string x is a url or not
def isWeb(x):
    return (x.startswith('https://') or x.startswith('http://'))


# dowload file from url using requests and display progress bar with tqdm
def tqdmDownload(url):
    try:
        response = requests.get(url, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size_in_bytes,
                            bar_format='{l_bar}{bar:50}{r_bar}', unit='iB', unit_scale=True)
        buffer = io.BytesIO()
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            buffer.write(data)
        progress_bar.close()

        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print('Error: failed to download')
            raise RuntimeError('failed to download')
        else:
            buffer.seek(0)
            return buffer
    except:
        raise


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
            bootUrl = os.path.join(
                bootSource, 'download', version, 'BOOT.BIN') + zynq
            print("Downloading BOOT.BIN from", bootUrl)
            bootF = tqdmDownload(bootUrl)
        else:
            print("Loading BOOT.BIN from", bootSource)
            with open(bootSource, mode='rb') as boot:
                bootF = io.BytesIO(boot.read())
    except:
        print('Error: invalid BOOT.BIN source or failed to load BOOT.BIN')
        raise

    global imageF
    try:
        if (isWeb(imageSource)):
            imageUrl = os.path.join(
                imageSource, 'download', version, 'image.ub') + zynq
            print("Downloading image.ub from", imageUrl)
            imageF = tqdmDownload(imageUrl)
        else:
            print("Loading image.ub from", imageSource)
            with open(imageSource, mode='rb') as image:
                imageF = io.BytesIO(image.read())
    except:
        print('Error: invalid image.ub source or failed to load image.ub')
        raise

    global tarF
    try:
        if (isWeb(tarSource)):
            tarUrl = os.path.join(tarSource, 'download',
                                  version, 'SD_p2.tar.gz') + zynq
            print("Downloading SD_p2.tar.gz from", tarUrl)
            tarF = tqdmDownload(tarUrl)
        else:
            print("Loading SD_p2.tar.gz from", tarSource)
            with open(tarSource, mode='rb') as tar:
                tarF = io.BytesIO(tar.read())
    except:
        print('Error: invalid SD_p2.tar.gz source or failed to load SD_p2.tar.gz')
        raise


def writeFiles(targetDir):
    if not os.path.exists(targetDir):
        os.makedirs(targetDir)

    dirFw = os.path.join(targetDir, 'fw')
    if not os.path.exists(dirFw):
        os.makedirs(dirFw)

    dirBoot = os.path.join(dirFw, 'BOOT.BIN')
    print('Writing BOOT.BIN to', dirBoot)
    with open(dirBoot, 'wb') as boot:
        boot.write(bootF.read())

    dirImage = os.path.join(dirFw, 'image.ub')
    print('Writing image.ub to', dirImage)
    with open(dirImage, 'wb') as image:
        image.write(imageF.read())

    print('Extracting SD_p2.tar.gz to', targetDir)
    with tarfile.open(fileobj=tarF, mode='r:gz') as tar:
        for member in tqdm(iterable=tar.getmembers(), total=len(tar.getmembers()), bar_format='{l_bar}{bar:50}{r_bar}'):
            if member.isfile() and os.path.exists(os.path.join(targetDir, member.name)):
                os.unlink(os.path.join(targetDir, member.name))
            tar.extract(member=member, path=targetDir, numeric_owner=True)


if __name__ == '__main__':
    main()
