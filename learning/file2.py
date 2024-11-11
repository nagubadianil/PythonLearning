import os

if os.path.isfile('myfile.txt'):
    print("It's a file")
else:
    print("files does not exist")
    
if os.path.isdir('mydir'):
    print("It's a directory")
else:
    print("The directory does not exist")

# os.mkdir('mydir')
# os.remove('myfile.txt')
# os.rename('myfile.txt', 'myfile_renamed.txt')

import shutil

shutil.move('/mnt/filesystem1/myfile.txt', '/mnt/filesystem2/mydir')

# Move to a directory, keeping the name intact
shutil.move('/home/erik/myfile.txt', '/home/erik/backups/')
# Copy a single file
shutil.copy('/home/erik/myfile.txt', '/home/erik/myfile_copy.txt')
# Copy entire tree of files
shutil.copytree('mydir', 'mydir_copy')
# Remove a tree of files
shutil.rmtree('mydir')