import sys
import os

# Get the absolute path of the project root (bus_app)
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Manually insert it into the system path
if root_path not in sys.path:
    sys.path.insert(0, root_path)