import sys
import os

# change this to absolute path of req_helper.py
req_helper = r"C:\Dev\Experiments\Python Learning\req_helper\req_helper.py"

sys.path.insert(0, os.path.dirname(req_helper))
from req_helper import write_requirements

# import your main entry file. Typically it is main
import main

print("Now write requirements.txt ...")
write_requirements()
print("Complete writing!")