import sys
import os
sys.path.insert(0, os.path.dirname(r"C:\Dev\Experiments\Python Learning\req_helper\req_helper.py"))
from req_helper import write_requirements

import main

print("Now write requirements.txt...")
write_requirements()
print("Complete writing!")