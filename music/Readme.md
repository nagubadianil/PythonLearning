

Make sure these folder exist
    root_folder = C:\Users\nagub\Music\Telugu
    root_folder_release = C:\Users\nagub\Music\Telugu_Release
    root_folder_voice_separated = C:\Users\nagub\Music\Telugu_Voice_Separated

1. Put the MP3s in root_folder, aka C:\Users\nagub\Music\Telugu folder.
2. Run this colab: https://colab.research.google.com/drive/1tIzmqshQKzc49QNmaIf5a0ZUbB_6dMKU
    a. Make sure to Add your root_folder, aka C:\Users\nagub\Music\Telugu, to Google Drive for syncing
    b. Make sure to Add music,aka "C:\Dev\Experiments\Python Learning\music", to Google Drive for syncing
3. Run music\transcribe_title\main.py run_once
4. Run music\reorganize\vocals.py delete
5. Run music\reorganize\accomp.py move
6. Run music\reorganize\release.py move
7. Delete files. (you can use music\reorganize\empty.py, but there appears to be bug )
