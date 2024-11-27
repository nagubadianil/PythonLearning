import os
import shutil
import sys

def move_accompaniment_files(root_folder, root_folder_voice_separated, list_only=False):
    # Walk through the root_folder and its subdirectories
    count = 0
    errcount = 0
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for file in filenames:
            if file.startswith("__accompaniment__"):  # Check if the file starts with "__accompaniment__"
                # Construct the full source file path
                src_file_path = os.path.join(dirpath, file)
                
                # Calculate the relative path from root_folder
                relative_path = os.path.relpath(dirpath, root_folder)
                
                # Construct the destination directory and file path
                dest_dir_path = os.path.join(root_folder_voice_separated, relative_path)
                dest_file_path = os.path.join(dest_dir_path, file)
                
                if not list_only:
                    # Ensure the destination directory exists
                    os.makedirs(dest_dir_path, exist_ok=True)
                    
                    # Move the file
                    try:
                        shutil.move(src_file_path, dest_file_path)
                        count+=1
                        print(f"{count} Moved: {src_file_path} \n-> {dest_dir_path}\n\n")
                        
                    except Exception as e:
                        errcount+=1
                        print(f"{errcount} Error moving {src_file_path}: {e}\n\n")
                else:
                    count+=1
                    print(f"{count} Source: {src_file_path}")
                    print(f"{count} Dest: {dest_dir_path}")
                        
def run_move_every_30_mins():
    from datetime import datetime
    import pytz  
    import time
    count = 1 
    
    root_folder = "C:/Users/nagub/Music/Telugu"
    root_folder_voice_separated = "C:/Users/nagub/Music/Telugu_Voice_Separated"
    while True:
        cst_timezone = pytz.timezone("US/Central")
        now_cst = datetime.now(cst_timezone)
        formatted_time = now_cst.strftime("%B %d, %Y %I:%M:%S %p")
        print("*"*70)
        print("*"*70)
        print(f"{count} Started new  run: ", formatted_time)
        
        try:
            move_accompaniment_files(root_folder, root_folder_voice_separated)   
        except Exception as e:
            print("EXCEPTION e:" + str(e))
            
        print("^"*70)
        print("^"*70)
        cst_timezone = pytz.timezone("US/Central")
        now_cst = datetime.now(cst_timezone)
        formatted_time = now_cst.strftime("%B %d, %Y %I:%M:%S %p")
        
        print(f"{count} Waiting... for 1 hour... started at: ", formatted_time)
        time.sleep(3600/2) 
        count+=1

if __name__=="__main__":
    root_folder = "C:/Users/nagub/Music/Telugu"
    root_folder_voice_separated = "C:/Users/nagub/Music/Telugu_Voice_Separated"
    if len(sys.argv) > 1:
        if sys.argv[1] == "loop":
            run_move_every_30_mins()
        elif sys.argv[1] == "move":
            move_accompaniment_files(root_folder, root_folder_voice_separated)  
        elif sys.argv[1] == "list":
             move_accompaniment_files(root_folder, root_folder_voice_separated,list_only=True)
        else:
            print("Your arguments didn't make sense")
    else:  
        pass
                 
