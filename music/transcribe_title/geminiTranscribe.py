import google.generativeai as genai
import os
import eyed3
import time

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
    
    """
    response = generate_transcription(prompt, mp3_file_path)
   
    print("#"*60)
    print(response.text)  # Output the transcription
    print("+"*60)
    print(response.usage_metadata)
    return response.text

def rename_and_add_metadata(lyrics_text, meta_data, mp3_file_path):
   
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

def parse_metadata(text):

    metadata = {}
    lines = text.strip().split("\n")
    for line in lines:
        # Split key and value by the first occurrence of ":"
        if ':' in line:
            key, value = line.split(":", 1)
            if "Not Found" in value:
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
    
def test_extract():
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
    mp3_file_path = "vocals.mp3"
    add_meta_data_to_mp3(response_text, mp3_file_path)

def transcribe_and_add_meta_data(vocals_file_path = "vocals.mp3", destination_file_path = "vocals.mp3"):
     
     response_text = get_media_information(vocals_file_path)
     add_meta_data_to_mp3(response_text, destination_file_path)


if __name__=="__main__":   
    #transcribe_audio()
    #add_meta_data_to_mp3()
    #get_media_information()
    #test_extract()
    
    transcribe_and_add_meta_data()
    
    """
    Play
    document.querySelector("#cell-hhqHhC3_U3Do > div.main-content > div > div.codecell-input-output > div.inputarea.horizontal.layout.code > div.cell-gutter > div > colab-run-button")
    
    Code cell
    document.querySelector("#cell-hhqHhC3_U3Do > div.main-content > div > div.codecell-input-output > div.inputarea.horizontal.layout.code > div.editor.flex.lazy-editor > div")
    """