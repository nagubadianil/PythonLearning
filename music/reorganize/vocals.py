import os
import sys


def iterator_vocals(root_folder):
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for file in filenames:
            if file.startswith("__vocal__"):  # Check if the file starts with "__vocal__"
                file_path = os.path.join(dirpath, file)  # Get full path of the file
                yield file_path

def delete_vocal_files(root_folder, list_only=False):

    for i, file_path in enumerate(iterator_vocals(root_folder)):
        if not list_only:
            try:
                os.remove(file_path)  # Delete the file
                print(f"{i}. Deleted: {file_path}")
            except Exception as e:
                print(f"{i}. Error deleting {file_path}: {e}")
        else:
            print(f"{i}. {file_path}")


def run_delete_every_30_mins():
    from datetime import datetime
    import pytz  
    import time
    count = 1 
    
    root_folder = "C:/Users/nagub/Music/Telugu"
    while True:
        cst_timezone = pytz.timezone("US/Central")
        now_cst = datetime.now(cst_timezone)
        formatted_time = now_cst.strftime("%B %d, %Y %I:%M:%S %p")
        print("*"*70)
        print("*"*70)
        print(f"{count} Started new  run: ", formatted_time)
        
        try:
            delete_vocal_files(root_folder)     
        except Exception as e:
            print("EXCEPTION e:" + str(e))
            
        print("^"*70)
        print("^"*70)
        cst_timezone = pytz.timezone("US/Central")
        now_cst = datetime.now(cst_timezone)
        formatted_time = now_cst.strftime("%B %d, %Y %I:%M:%S %p")
        
        print(f"{count} Waiting... for 30mins... started at: ", formatted_time)
        time.sleep(3600/2) 
        count+=1

if __name__=="__main__":
    root_folder = "C:/Users/nagub/Music/Telugu"
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "loop":
            run_delete_every_30_mins()
        elif sys.argv[1] == "delete":
            delete_vocal_files(root_folder)
        elif sys.argv[1] == "list":
            delete_vocal_files(root_folder, list_only=True)
        else:
            print("Your arguments didn't make sense")
    else:
        for file in  iterator_vocals(root_folder):
            print(file)