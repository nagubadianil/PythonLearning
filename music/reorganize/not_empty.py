
import os
from  empty import list_empty_folders_in_voice_separated
import sys


def list_not_empty_files( root_folder = "C:/Users/nagub/Music/Telugu"):
   
    empty_voice_separated,full_voice_separated_folders = list_empty_folders_in_voice_separated(root_folder)

    for voice_separated in full_voice_separated_folders:
        print(f"{voice_separated}")
        for dirpath, dirnames, filenames in os.walk(voice_separated):
            for file in filenames:
                print(f"Files in __VS__:{os.path.join(dirpath, file)}")
    
        parent=os.path.dirname(voice_separated)
        for parent_file in os.listdir(parent):
            print(f"PARENT of __VS__:{parent_file}")
        
        
if __name__ == "__main__":
    root_folder = "C:/Users/nagub/Music/Telugu"
    if len(sys.argv) > 1:
        if sys.argv[1] == "list":
            list_not_empty_files(root_folder)
        else:
            print("Your arguments didn't make sense")
    else:  
        pass
                 