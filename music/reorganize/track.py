import os
import sys

def iterator_vocals_mp3(root_folder):
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for file in filenames:
            if file == "vocals.mp3":  # Check if the file is named vocals.mp3
                
                yield os.path.join(dirpath,file)
    
def find_missing_mp3_for_vocal():
    root_folder = "C:/Users/nagub/Music/Telugu"
    count = 0
    good = 0
    for vocal in iterator_vocals_mp3(root_folder):
        #print(f"vocal: {vocal}")    
        parent_folder = os.path.dirname(vocal)
        mp3_name = os.path.basename(parent_folder)
        mp3_location = os.path.dirname(os.path.dirname(parent_folder))
        
        mp3_file_path = os.path.join(mp3_location, mp3_name+".mp3")
    
        if not os.path.isfile(mp3_file_path):
            count+=1
            print(f"{count} ERROR: {mp3_file_path}")
        else:
            good+=1
            #print(f"GOOD: {mp3_file_path}")
            
    print(f"good: {good} missing: {count}")


def count_vocals_files(root_folder):
    count = 0
    # Traverse the folder and subfolders
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for file in filenames:
            if file == "vocals.mp3":  # Check if the file is named vocals.mp3
                count += 1
    return count

def list_all_track_files():
    root_folder = "C:/Users/nagub/Music/Telugu"
    total_count = 0
    
    for dirpath, _, filenames in os.walk(root_folder):
        exists = 0
        mp3_count = 0
        
        #print(f"\n\ndirpath: {dirpath}")
        for  filename in filenames:
            if "track_" in filename and ".mp3" in filename:
                #print(f"{i} : {os.path.join(dirpath, filename)}")
                total_count+=1
                exists = 1
                mp3_count+=1
        
        if exists == 1:
            voice_separated_path = os.path.join(dirpath, "__Voice_Separated__")
            vocals_count = count_vocals_files(voice_separated_path)
            
            print(f"mp3_count: {mp3_count} vocals_count: {vocals_count}")
            if mp3_count != vocals_count:
                print("**** ERROR: Count of vocals does not equal to mp3_count")
            else:
                print("")
    print("Total track files: ", total_count)

if __name__=="__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "missing":
            find_missing_mp3_for_vocal()
        elif sys.argv[1] == "tracks":
            list_all_track_files()
        elif sys.argv[1] == "count_vocals":
            root_folder = "C:/Users/nagub/Music/Telugu"
            count = count_vocals_files(root_folder)
            print(f"Vocals.mp3 count: {count}")
        else:
            print("Your arguments didn't make sense")
    else:  
        pass
                 