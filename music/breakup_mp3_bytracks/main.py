from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import sys
"""

Must install ffmpeg on system: 
 Instructions: https://phoenixnap.com/kb/ffmpeg-windows    

 binaries location: https://www.gyan.dev/ffmpeg/builds/

"""
# Function to split MP3 file based on pauses
def split_mp3(file_path, output_folder, min_silence_len=1000, silence_thresh=-40):
    """
    Splits an MP3 file into segments where there are pauses (silence).

    Parameters:
    - file_path: Path to the MP3 file.
    - output_folder: Folder to save the split tracks.
    - min_silence_len: Minimum length of silence (in ms) to be considered a split point.
    - silence_thresh: Silence threshold (in dBFS, relative to max volume) to detect silence.
    """
    try:
        # Load the audio file
        audio = AudioSegment.from_mp3(file_path)
        
        # Split audio on silence
        chunks = split_on_silence(
            audio,
            min_silence_len=min_silence_len,
            silence_thresh=silence_thresh
        )
        
        # Save the split audio files
        for i, chunk in enumerate(chunks):
            output_file = f"{output_folder}/track_{i+1}.mp3"
            chunk.export(output_file, format="mp3")
            print(f"Saved: {output_file}")
        
        print("Splitting complete!")
    except Exception as e:
        print(f"An error occurred: {e}")



def find_long_mp3_files(folder_path, duration_threshold_minutes=9):
    """
    Detects MP3 files in a folder that are longer than the specified duration.

    Parameters:
    - folder_path: Path to the folder containing MP3 files.
    - duration_threshold_minutes: Duration threshold in minutes to filter files.

    Returns:
    - List of file paths for MP3 files exceeding the duration threshold.
    """
    long_files = []
    duration_threshold_ms = duration_threshold_minutes * 60 * 1000  # Convert to milliseconds

    try:
        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith('.mp3'):
                file_path = os.path.join(folder_path, file_name)
                
                # Load the MP3 file
                audio = AudioSegment.from_mp3(file_path)
                duration = len(audio)  # Duration in milliseconds
                
                # Check if the duration exceeds the threshold
                if duration > duration_threshold_ms:
                    long_files.append(file_path)
                    print(f"File: {file_name}, Duration: {duration // 1000 // 60} min")
        
        if not long_files:
            print("No files found exceeding the duration threshold.")
        return long_files
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def create_folder_for_file(file_path):
    """
    Creates a folder in the same directory as the given file, with the folder name
    matching the file name (without the extension).

    Parameters:
    - file_path: Path to the file.

    Returns:
    - Path to the created folder.
    """
    try:
        # Get the directory and file name without the extension
        folder_path = os.path.splitext(file_path)[0]

        # Create the folder if it doesn't already exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Folder created: {folder_path}")
        else:
            print(f"Folder already exists: {folder_path}")
        
        return folder_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def split_all_files_in_folder():
    # Example usage
    root_folder = "c:/Users/nagub/Music/Telugu/DSP"  # Replace with your folder path
    
    if len(sys.argv)>1 and sys.argv[1] is not None:
        root_folder = sys.argv[1]
    
    
    long_mp3_files = find_long_mp3_files(root_folder)

    print("\nFiles longer than 9 minutes:")
    for file_path in long_mp3_files:
        print("mp3 file: ", file_path)
        folder_path = create_folder_for_file(file_path)
        print("Where mp3 splits be stored: ", folder_path)
        
        if folder_path is not None:
            split_mp3(file_path, folder_path)    

def test1():
    file_path="c:/Users/nagub/Music/Telugu/DSP\Allu Arjun & Devi Sri Prasad Hit Songs  So Satyamurthy Movie Special.mp3"
    folder_path="c:/Users/nagub/Music/Telugu/DSP\Allu Arjun & Devi Sri Prasad Hit Songs  So Satyamurthy Movie Special"
    split_mp3(file_path, folder_path)    

if __name__=="__main__":
    #test1()
    split_all_files_in_folder()
