import eyed3
import os
import sys

def has_lyrics(mp3_file_path):
    
    audiofile = eyed3.load(mp3_file_path)
    
    if audiofile is None:
        return False
    
    if audiofile.tag is None:
        audiofile.tag = eyed3.id3.tag.ID3Tag()
    
    
    if audiofile.tag.lyrics and len(audiofile.tag.lyrics) != 0:        
        lyrics = audiofile.tag.lyrics[0]
        if len(lyrics.text) != 0:
            #print(f"Has Lyrics. File: {mp3_file_path}")
            return True
    return False    

def iterator_for_lyrics(root_folder, have_lyrics):
    for dirpath, dirnames, filenames in os.walk(root_folder):
        for file in filenames:
            
            if "__Voice_Separated__" in dirpath:
                continue
            
            if ".mp3" not in file:
                continue
            mp3_file_path = os.path.join(dirpath, file)
            #print(f"\n\nmp3_file_path: {mp3_file_path}")
            does_have_lyrics = has_lyrics(mp3_file_path)
                
            if have_lyrics and does_have_lyrics:
                yield mp3_file_path
            elif not have_lyrics and not does_have_lyrics:
                yield mp3_file_path
    
def test_iterator(root_folder, has_lyrics):
    for i, mp3_file in enumerate(iterator_for_lyrics(root_folder, has_lyrics)):
        print(f"{i+1}. ",mp3_file)                   
   
            
def test_has_lyrics():
    mp3_file_path = r"C:\Users\nagub\Music\Telugu_Release\Keeravani\Duvvina Talane Full Song - Naa Autograph Telugu Movie -  Ravi Teja, Bhoomika.mp3"
    verdict = has_lyrics(mp3_file_path)
    print(f"verdict: {verdict}")
    
    mp3_file_path = r"C:\Users\nagub\Music\Telugu_Release\Keeravani\Sri Ramadasu Video Songs - Ilalo Nee Namasmaranam Song - Nagarjuna Akkineni,Sneha.mp3"
    verdict = has_lyrics(mp3_file_path)
    
    print(f"verdict: {verdict}")


if __name__=="__main__":
    root_folder_release = r"C:\Users\nagub\Music\Telugu_Release"
    root_folder = r"C:\Users\nagub\Music\Telugu"
    if len(sys.argv) > 1:
        if sys.argv[1] == "check_lyrics":
            mp3_file_path=""
            has_lyrics(mp3_file_path)
        elif sys.argv[1] == "list":
            test_iterator(root_folder, has_lyrics=True)
        elif sys.argv[1] == "list_no_lyrics":
            test_iterator(root_folder, has_lyrics=False)
        elif sys.argv[1] == "list_release":
            test_iterator(root_folder_release, has_lyrics=True)
        elif sys.argv[1] == "list_release_no_lyrics":
            test_iterator(root_folder_release, has_lyrics=False)
        else:
            print("Your arguments didn't make sense")
    else:  
        pass
                 


