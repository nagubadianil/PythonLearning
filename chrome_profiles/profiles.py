import os
import json

# Path to Chrome's user data directory
user_data_dir = r"C:\Users\nagub\AppData\Local\Google\Chrome\User Data"

# Iterate through profile folders
for profile in os.listdir(user_data_dir):
    preferences_path = os.path.join(user_data_dir, profile, "Preferences")
    if os.path.isfile(preferences_path):
        with open(preferences_path, "r", encoding="utf-8") as f:
            try:
                prefs = json.load(f)
                email = prefs.get("profile", {}).get("gaia_info", {}).get("email")
                name = prefs.get("profile", {}).get("name")
                if email:
                    print(f"Profile: {profile} | Name: {name} | Email: {email}")
            except json.JSONDecodeError:
                continue
