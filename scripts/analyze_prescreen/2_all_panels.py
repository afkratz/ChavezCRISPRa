import subprocess
import os
from pathlib import Path

os.chdir(Path(__file__).resolve().parent)
subprocess.call("python 2_a.py", shell=True)
subprocess.call("python 2_b.py", shell=True)
subprocess.call("python 2_c.py", shell=True)
subprocess.call("python 2_d.py", shell=True)
subprocess.call("python 2_e.py", shell=True)
subprocess.call("python 2_f.py", shell=True)
subprocess.call("python 2_g.py", shell=True)
subprocess.call("python 2_h.py", shell=True)
subprocess.call("python 2_i.py", shell=True)
