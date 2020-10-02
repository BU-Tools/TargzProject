from urllib import request # request for targz file
import tarfile # open tar file
import io # bytesIO object
import sys # error handling



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
                tar.extract(filepath)
            except KeyError:
                print("Invalide file path")
            except:
                print("Unexpected error: ", sys.exc_info()[0])
        else:
            print("Invalid command type help for list of commands")
    

    tar.close()
