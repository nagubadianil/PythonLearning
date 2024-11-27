import os
import shutil
import stat
import sys


def delete_regular_empty_dirs(root_folder, list_only=False):
    count = 0
    errcount = 0
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for dirname in dirnames:
            cur_dir_full_path = os.path.join(dirpath, dirname)
            
            if "__Voice_Separated__" in cur_dir_full_path:
                continue
            
            if not os.listdir(cur_dir_full_path):
                if not list_only:
                    try:
                        shutil.rmtree(cur_dir_full_path, onexc=remove_readonly)
                        count+=1
                        print(f"{count}. Deleted: {cur_dir_full_path}")
                    except FileNotFoundError:
                        errcount+=1
                        print(f"{errcount}. Folder not found: {cur_dir_full_path}")
                    except Exception as e:
                        errcount+=1
                        print(f"{errcount}. Delete Error occurred: {e}")
                else:
                    count+=1
                    print(f"{count}. {cur_dir_full_path}")
                    
    if not list_only:                
        print(f"Deleted count {count} Error: {errcount}")
                
def list_empty_folders_in_voice_separated(root_folder):
    
    empty_voice_separted_folders = set()
    all_voice_separated_folders = set()
    
    # Walk through the directory tree
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for dirname in dirnames:
            if dirname == "__Voice_Separated__":
                voice_separated_path = os.path.join(dirpath, dirname)
                all_voice_separated_folders.add(voice_separated_path)
                # Iterate over all child folders in __Voice_Separated__
                
                if not os.listdir(voice_separated_path):
                    empty_voice_separted_folders.add(voice_separated_path)
                else:
                    for child in os.listdir(voice_separated_path):
                        child_path = os.path.join(voice_separated_path, child)
                        if os.path.isdir(child_path) and not os.listdir(child_path):  # Check if folder is empty
                            try:
                                empty_voice_separted_folders.add(voice_separated_path)
                          
                            except Exception as e:
                                print(f"Error deleting folder {child_path}: {e}\n\n")
                            
    full_voice_separated_folders = all_voice_separated_folders - empty_voice_separted_folders
    return empty_voice_separted_folders, full_voice_separated_folders

def remove_readonly(func, path, _):
        os.chmod(path, stat.S_IWRITE)  # Add write permission
        func(path)

def delete_all_voice_separate(root_folder = "C:/Users/nagub/Music/Telugu"):
    
   
    empty_voice_separated,full_voice_separated_folders  = list_empty_folders_in_voice_separated(root_folder)  
    
    count=0
    errcount = 0
    for dir_path in empty_voice_separated:
       
        try:
            shutil.rmtree(dir_path, onexc=remove_readonly)
            count+=1
            print(f"{count}. Deleted: {dir_path}")
        except FileNotFoundError:
            errcount+=1
            print(f"{errcount}. Folder not found: {dir_path}")
        except Exception as e:
            errcount+=1
            print(f"{errcount}. Delete Error occurred: {e}")
    
    print(f"Deleted count {count} Error: {errcount}")

def list_voice_separate_emptys(root_folder = "C:/Users/nagub/Music/Telugu"):
    
    empty_voice_separated,full_voice_separated_folders  = list_empty_folders_in_voice_separated(root_folder)  
   
    print("EMPTY __Voice_Separated__:")
    for i, f in enumerate(empty_voice_separated):
        print(f"{i} : {f}")
    
    print("#"*70)
    
    print("FULL __Voice_Separated__:")
    for i, f in enumerate(full_voice_separated_folders):
        print(f"{i} : {f}")

#list_voice_separate_emptys
if __name__=="__main__":
    root_folder = "C:/Users/nagub/Music/Telugu"
    if len(sys.argv) > 1:
        if sys.argv[1] == "list":
            list_voice_separate_emptys(root_folder)
        elif sys.argv[1] == "delete":
            delete_all_voice_separate(root_folder)
        elif sys.argv[1] == "delete_reg":
            delete_regular_empty_dirs(root_folder, list_only=False)
        elif sys.argv[1] == "list_reg":
            delete_regular_empty_dirs(root_folder, list_only=True)    
        else:
            print("Your arguments didn't make sense")
    else:  
        pass