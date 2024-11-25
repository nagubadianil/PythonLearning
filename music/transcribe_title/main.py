from spleeter.separator import Separator
import os
"""
Install disutils first
    https://visualstudio.microsoft.com/visual-cpp-build-tools/

Install in Code environment using Python 3.10
    conda create -n spleeter_env python=3.10 -y
    conda activate spleeter_env
    
    pip install wheeler_file\spleeter-2.4.0-py3-none-any.whl

    command line:
     python -m spleeter separate 
"""
def separate_vocals_from_music(mp3_file_path, output_folder):
    """
    Separates vocals from music using Spleeter and saves them as separate MP3 files.
    
    Parameters:
    - mp3_file_path: Path to the input MP3 file.
    - output_folder: Folder where the separated tracks will be saved.
    
    Returns:
    - None
    """
    try:
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Initialize the separator (2stems mode: vocals + accompaniment)
        separator = Separator('spleeter:2stems')

        # Perform the separation (this will create two files: vocals and accompaniment)
        separator.separate_to_file(mp3_file_path, output_folder)
        
        # Notify user of successful separation
        print(f"Separation complete! Files saved in {output_folder}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    mp3_path = "C:/Users/nagub/Music/Telugu/DSP/Allu Arjun & Devi Sri Prasad Hit Songs  So Satyamurthy Movie Special/track_2.mp3"
    
    # Replace with the path to your MP3 file
    output_folder = "C:/Users/nagub/Music/separate_voice_music"  # Replace with the folder to save the separated tracks
    separate_vocals_from_music(mp3_path, output_folder)
#  python -m spleeter separate -o output/ track_3.mp3 
 