#!/user/bin/env python3
from urllib import request # request for targz file
import tarfile # open tar file
import io # bytesIO object
import sys # error handling

import argparse
from argparse import RawTextHelpFormatter





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
                        default='v1.4.2',
                        help='version of BOOT.BIN, image.ub, and SD_p2.tar.gz, ignored when source is local directory')
    parser.add_argument('-zynq', type=str, 
                        default='v1.4.2',
                        help='zynq of BOOT.BIN and image.ub, ignored when source is local directory')
    parser.add_argument('-dir', type=str, 
                        default='./',
                        help='directory which the files will be written to\ntar.gz files will be written to DIR, BOOT.BIN and image.ub will be written to DIR/fw')

    args = parser.parse_args()
    print(args.boot, args.image, args.tar, args.ver, args.dir, sep='\n')

    getFiles(args)
    writeFiles(args.dir)

def isWeb(str):
    return str.startsWith("https://")

def getFiles(args):
    bootSource = args.boot.strip()
    imageSource = args.image.strip()
    tarSource = args.tar.strip()
    version = args.ver.strip()
    zynq = args.zynq.strip()

    if zynq:
        zynq = '.' + zynq

    if (isWeb(bootSource)):
        res = request.urlopen(bootSource+'download/v'+version+'/BOOT.BIN'+zynq)
        with res as r:
            bootF = io.BytesIO(r.read()) 
    else:


    if (isWeb(imageSource)):
        res = request.urlopen(bootSource+'download/v'+version+'/image.ub'+zynq)
        with res as r:
            imageF = io.BytesIO(r.read()) 
    else:


    if (isWeb(tarSource)):
        res = request.urlopen(bootSource+'download/v'+version+'/SD_p2.tar.gz')
        with res as r:
            tarF = io.BytesIO(r.read()) 
    else:




def writeFiles(dir):




url = "https://github.com/apollo-lhc/SM_ZYNQ_FW/releases/download/v1.4.2/SD_p2.tar.gz"
response = request.urlopen(url)

print("Response code: ", response.getcode())
print("Downloaded: ", response.info().get_filename())

with response as r: 
    print('Extracting data, this may take a while, please wait...')
    r = io.BytesIO(r.read()) # convert response data to bytesIO object for random access
    tar = tarfile.open(fileobj=r, mode='r:gz') # Decompress response to tar file
    members = tar.getmembers()
    print("Done!")

    while True:
        command = input("\nEnter a command (type help for list of commands): ")
        command = command.strip()
        if (command == 'quit'):
            break
        elif (command == 'help'):
            print("getInfo --- get the info of a file", "getFile --- print out a file", "extractFile --- extract a file to disk", "quit --- quit the program", sep='\n')
        elif (command == 'getInfo'):
            try:
                filepath = input("Enter a file path: ")
                fileMember = tar.getmember(filepath)
                print(fileMember.name)
                print(fileMember.size)
                print(fileMember.mtime)
            except KeyError:
                print("Invalide file path")
            except:
                print("Unexpected error: ", sys.exc_info()[0])
        elif (command == 'getFile'):
            try: 
                filepath = input("Enter a file path: ")
                fileMember = tar.extractfile(filepath)
                with fileMember as f:
                    lines = [line.decode('utf-8').rstrip() for line in f]
                print(*lines, sep='\n')
            except KeyError:
                print("Invalide file path")
            except:
                print("Unexpected error: ", sys.exc_info()[0])
        elif (command == 'extractFile'):
            try: 
                filepath = input("Enter a file path: ")
                tar.extract(filepath, numeric_owner=True)
            except KeyError:
                print("Invalide file path")
            except:
                print("Unexpected error: ", sys.exc_info()[0])
        else:
            print("Invalid command type help for list of commands")
    

    tar.close()



if __name__ == '__main__':
    main()