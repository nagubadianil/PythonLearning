import google.generativeai as genai
import os
import eyed3
import time
import re
import sys

# Configure with your API key
genai.configure(api_key="AIzaSyD99y8NSlHxoP3p-zlhrkvh3PTIXh7c6sE")
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_transcription(prompt, mp3_file_path=None):

    sample_audio = None
    if mp3_file_path is not None:
        sample_audio = genai.upload_file(mp3_file_path)

        while sample_audio.state.name == "PROCESSING":
                print("uploaded, now processing video...")
                time.sleep(2)
                sample_audio = genai.get_file(sample_audio.name)
                
    response = model.generate_content([prompt,sample_audio])
    return response


def get_media_information(mp3_file_path):
    prompt = """
    You are a music researsch assistant. I need two things to be done from you.
    First, transcribe this for me. Only transcribe it in english text and put it in response, without any other text or preamble.
    Then add "-------------------" in response on a  new line.
    Then do the below:
    Given the transcription, do an internet search and find out Title, Album, Artist, Genre, Language, Year 
    Make sure to put them in one line each in response. Don't put any other text like preamble or anything
    Also, if you cannot determine the values for them, just put "Not Found". Don't put other text.
    """
    try:
        response = generate_transcription(prompt, mp3_file_path)
        
        #print(response)
        print("#"*60)
        print(response.text)  # Output the transcription
        print("+"*60)
        print(response.usage_metadata)
        return response.text
    except Exception as e:
      print("$"*90)
      print("get_media_information Exception e:", str(e))
      print("$"*90) 
      return "Exception:"+str(e)  
 
def sanitize_filename(filename):
    # For Windows, remove invalid characters: \ / : * ? " < > |
    windows_invalid_chars = r'[<>:"/\\|?*]'
    
    # For Linux and macOS, remove the forward slash if present in filenames
    linux_mac_invalid_chars = r'[\/]'
    
    # Replace invalid characters with an underscore (_)
    sanitized_filename = re.sub(windows_invalid_chars, '_', filename)  # Replace Windows invalid chars
    sanitized_filename = re.sub(linux_mac_invalid_chars, '_', sanitized_filename)  # Replace / for Linux/Mac paths
    
    # Remove control characters (non-printable)
    sanitized_filename = re.sub(r'[\x00-\x1F\x7F]', '', sanitized_filename)
    
    # Trim leading/trailing spaces
    sanitized_filename = sanitized_filename.strip()

    # Handle reserved names for Windows (e.g., CON, PRN, AUX, etc.)
    reserved_names = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
    if sanitized_filename.upper() in reserved_names:
        sanitized_filename = f'_{sanitized_filename}'

    return sanitized_filename


def rename_and_add_metadata(lyrics_text, meta_data, mp3_file_path):

    try:
        # Load the MP3 file
        audiofile = eyed3.load(mp3_file_path)
        
        # Ensure there is a tag (metadata) object
        if audiofile.tag is None:
            audiofile.tag = eyed3.id3.tag.ID3Tag()

        # Parse metadata (already parsed in the function above)
        title = meta_data.get("Title", "Not Found")
        genre = meta_data.get("Genre", "Not Found")
        language = meta_data.get("Language", "Not Found")
        album = meta_data.get("Album", "")
        artist = meta_data.get("Artist", "")
        year = meta_data.get("Year", "")

        # If Title is not found, use the first 10 words from lyrics
        if title == "Not Found":
            title = ' '.join(lyrics_text.split()[:10])
                
            title = title[:45]
            title = sanitize_filename(title)
            title = title.title()
            
        audiofile.tag.title = title  # Title case for Title

        # If Genre is not found, add "Telugu Songs"
        if genre == "Not Found":
            genre = "Telugu Songs"
        audiofile.tag.genre = genre

        # If Language is not found, add "Telugu"
        if language == "Not Found":
            language = "Telugu"
        audiofile.tag.language = language

        if artist == "Not Found":
            artist = ""
        audiofile.tag.artist = artist
        
        if album == "Not Found":
            album = ""
        audiofile.tag.album = album
        
        if year == "Not Found":
            year = ""
        audiofile.tag.year = year

        # Add the lyrics to the tag
        audiofile.tag.lyrics.set(lyrics_text)

        # Save the changes to the audio file
        audiofile.tag.save()

        new_file_path = mp3_file_path
        if "track_" in mp3_file_path:
            # Rename the MP3 file
            new_file_path = os.path.join(os.path.dirname(mp3_file_path), title+".mp3")
            os.rename(mp3_file_path, new_file_path)
            
        return new_file_path  # Return the new file path

    except Exception as e:
        print("$"*90)
        print("rename_and_add_metadata Exception e:", str(e))
        print("$"*90) 
        return "Exception:"+str(e)  
 
    
def parse_metadata(text):

    metadata = {}
    lines = text.strip().split("\n")
    bad_strings = [
        "Not Found",
        "not be found",
        "Unable to determine",
        "Unknown",
        "Not found",
    ]
    for line in lines:
        # Split key and value by the first occurrence of ":"
        if ':' in line:
            key, value = line.split(":", 1)
            #if "Not Found" in value or "not be found" in value or "Unable to determine" in value or "not be found" in value:
            if any(item in value for item in bad_strings):
                value = "Not Found"
            metadata[key.strip()] = value.strip()
    return metadata


def add_meta_data_to_mp3(response_text, mp3_file_path = "vocals.mp3"):
    # Example Usage
    resp_array = response_text.split("-------------------")
    lyrics_text = resp_array[0].strip()
    meta_data = parse_metadata(resp_array[1].strip())
    new_file_path = rename_and_add_metadata(lyrics_text=lyrics_text, meta_data=meta_data, mp3_file_path=mp3_file_path)
    print(f"New file created at: {new_file_path}")
    return new_file_path 
    
def test_extract(mp3_file_path = "vocals.mp3"):
    response_text = """
Hey natja venne isam bode nuvena rajakumari
Hey ajjare raja janile jare leta javanile
Hey natja venne isam bode nuvena rajakumari
Ajare raja janile jare leta javanile
Andis nekeli usari heges tagenu gambari
Seshis nechal usari sir pangau bisingari
Bangare sai andunde daiya daive yadhile
Natja venne isam bode nuvena rajakumari
Ajare raja janile jare leta javanile

Hey sadataka sasuk jeri sagista sukusa chori
Jalin du mataka jeri dusta du talupu jori
Umbirave mayal badhi
Murpis pela murari
Parigane mallu budani parigete kudase budani
Pili gare prema puja ari beli poda manasisi jari
Gundilloko vedage takulu undu bide vere
Natja venne isam bode nuvena rajakumari
Ajare raja janile jare leta javanile


Hey baradale andulugi vachaga topada yekori
Sudigaale niluvun nemani yagade sukupotani
Rathasta sinkulu leheri
Hey chelusta sukuna degeri
Mutululo jibosari pampululo jibosari
Vaigamulu sulivosani okeluba ni vosani
Navari bintare bade sei badhisari
Hey natja venne isam bode nuvena rajakumari
Ajare raja janile jare leta javanile


-------------------
Title:  Not Found (Likely a folk song or untitled piece)
Album: Not Found
Artist: Not Found
Genre: Folk
Language: Telugu
Year: Not Found
    """
    
    add_meta_data_to_mp3(response_text, mp3_file_path)

def transcribe_and_add_meta_data(vocals_file_path = "vocals.mp3", destination_file_path = "vocals.mp3"):
     
    response_text = get_media_information(vocals_file_path)
    if "Exception" not in response_text:
        return add_meta_data_to_mp3(response_text, destination_file_path)
    else:
        return response_text

def file_iterator(root_folder):

    for dirpath, _, filenames in os.walk(root_folder):
        for filename in filenames:
            # Yielding all files named 'vocals.mp3'
            if filename.lower() == 'vocals.mp3':
                vocals_path = os.path.join(dirpath, filename)
               
                parent_folder = os.path.dirname(vocals_path)  # Get the parent folder of 'vocals.mp3'
                parent_name = os.path.basename(parent_folder)
                great_grandparent_folder =  os.path.dirname(os.path.dirname(parent_folder))  # Get the grandparent folder
                
                mp3_path = os.path.join(great_grandparent_folder, parent_name+".mp3")
                yield vocals_path,mp3_path 

def rename_vocals(vocals_path,mp3_path):
        new_dir_name = os.path.basename(mp3_path).split(".mp3")[0]
        parent_folder = os.path.dirname(vocals_path) 
        parent_dir = os.path.dirname(parent_folder)
       
        new_path = os.path.join(parent_dir, new_dir_name)
        
        new_vocals_path = os.path.join(parent_folder, "__vocal__"+ new_dir_name + ".mp3")
        old_accompaniment_path = os.path.join(parent_folder, "accompaniment" + ".mp3")
        new_accompaniment_path = os.path.join(parent_folder, "__accompaniment__" + new_dir_name +".mp3")
        
        os.rename(vocals_path, new_vocals_path)
        os.rename(old_accompaniment_path, new_accompaniment_path)
        os.rename(parent_folder, new_path)
        
        return new_path 
def process_separated_files():
    root_folder = "C:/Users/nagub/Music/Telugu"
    count = 0
    skipcount = 0
    for vocals_path, mp3_path in file_iterator(root_folder):
        print(f"!!vocals: {vocals_path}")
        print(f"!!mp3_path {mp3_path}")
       
        new_mp3_path = transcribe_and_add_meta_data(vocals_file_path = vocals_path, destination_file_path = mp3_path)
        
        if "Exception" not in new_mp3_path:
            print(f"!!new_mp3_path:", new_mp3_path)
            
            new_vocals_root_path = rename_vocals(vocals_path, new_mp3_path)
            
            print(f"!!new_vocals_root_path:", new_vocals_root_path)
            print("+"*60)
            count+=1
        else:
            print(f"Skipping: {mp3_path}\n Error: {new_mp3_path}")
            skipcount+=1
    
    print(f"All Done, for now! count: {count} skipcount:{skipcount}")
        
def run_every_hour():
    from datetime import datetime
    import pytz  
    
    count = 1 
    while True:
        cst_timezone = pytz.timezone("US/Central")
        now_cst = datetime.now(cst_timezone)
        formatted_time = now_cst.strftime("%B %d, %Y %I:%M:%S %p")
        print("*"*70)
        print("*"*70)
        print(f"{count} Started new  run: ", formatted_time)
        
        try:
            process_separated_files()     
        except Exception as e:
            print("EXCEPTION e:" + str(e))
            
        print("^"*70)
        print("^"*70)
        cst_timezone = pytz.timezone("US/Central")
        now_cst = datetime.now(cst_timezone)
        formatted_time = now_cst.strftime("%B %d, %Y %I:%M:%S %p")
        
        print(f"{count} Waiting... for 1 hour... started at: ", formatted_time)
        time.sleep(3600) 
        count+=1
        
        
if __name__=="__main__":   
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "loop":
            run_every_hour()
        elif sys.argv[1] == "run_once":
            process_separated_files()
        elif sys.argv[1] == "add_meta_data":
            mp3_file_path = "vocals.mp3"
            test_extract(mp3_file_path)
        elif sys.argv[1] == "gen_info":
            mp3_file_path = "vocals.mp3"
            get_media_information(mp3_file_path)
        else:
            print("Your arguments didn't make sense")
    else:  
        pass
