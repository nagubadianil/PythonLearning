from  lyrics import iterator_for_lyrics, test_iterator
import os
import shutil
import sys



def move_good_to_release( root_folder = "C:/Users/nagub/Music/Telugu",
    root_folder_release = "C:/Users/nagub/Music/Telugu_Release", have_lyrics=True):
    
    mp3s_with_lyrics =  list(iterator_for_lyrics(root_folder, have_lyrics=have_lyrics))
    count = 0
    errcount = 0
    for mp3_file in mp3s_with_lyrics:
        path_to_good_folder = os.path.dirname(mp3_file)
        relative_path = os.path.relpath(path_to_good_folder, root_folder)   

        dest_dir_path = os.path.join(root_folder_release, relative_path)
        
        for f in os.listdir(path_to_good_folder):
            src_file_path = os.path.join(path_to_good_folder,f)
            if os.path.isfile(src_file_path):
                dest_file_path = os.path.join(dest_dir_path, f)
                
                try:
                    os.makedirs(dest_dir_path, exist_ok=True)
              
                    shutil.move(src_file_path, dest_file_path)
                    count+=1
                    
                    print(f"{count}. Source: {src_file_path}")
                    print(f"{count}. Dest  : {dest_dir_path}\n\n")   
                except Exception as e:
                    print(f"{errcount}. Error moving {src_file_path}: {e}\n\n")
   
    print(f"Move count: {count} Error: {errcount}")
                    
def run_move_good_to_release_every30mins():
    from datetime import datetime
    import pytz  
    import time
    count = 1 
    while True:
        cst_timezone = pytz.timezone("US/Central")
        now_cst = datetime.now(cst_timezone)
        formatted_time = now_cst.strftime("%B %d, %Y %I:%M:%S %p")
        print("*"*70)
        print("*"*70)
        print(f"{count} Started new  run: ", formatted_time)
        
        try:
            move_good_to_release()    
        except Exception as e:
            print("EXCEPTION e:" + str(e))
            
        print("^"*70)
        print("^"*70)
        cst_timezone = pytz.timezone("US/Central")
        now_cst = datetime.now(cst_timezone)
        formatted_time = now_cst.strftime("%B %d, %Y %I:%M:%S %p")
        
        print(f"{count} Waiting... for 30 mins... started at: ", formatted_time)
        time.sleep(3600/2) 
        count+=1
               
if __name__=="__main__":
    root_folder = "C:/Users/nagub/Music/Telugu"
    root_folder_release = "C:/Users/nagub/Music/Telugu_Release"
    if len(sys.argv) > 1:
        if sys.argv[1] == "move":
             move_good_to_release(root_folder, root_folder_release)
        elif sys.argv[1] == "list":   
            test_iterator(root_folder, has_lyrics=True)
        elif sys.argv[1] == "loop":
            run_move_good_to_release_every30mins()
        elif sys.argv[1] == "move_reverse_no_lyrics":
             move_good_to_release(root_folder_release, root_folder, have_lyrics=False)
        else:
            print("Your arguments didn't make sense")
    else:  
        pass
                 