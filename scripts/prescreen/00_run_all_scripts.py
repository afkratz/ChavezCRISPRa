import subprocess
import os
from pathlib import Path

os.chdir(Path(__file__).resolve().parent)
subprocess.call("python 01_run_uclust.py", shell=True)
subprocess.call("python 02_assign_hits_and_clusters.py", shell=True)
subprocess.call("python 03_charachterize_manual_tested_domains.py", shell=True)
subprocess.call("python 04_PADDLE_manual_tested_domains.py", shell=True)
subprocess.call("python 05_PADDLE_auroc.py", shell=True)
subprocess.call("python 06_biochem_hit_LR_model.py", shell=True)
subprocess.call("python 07_linear_biochem_characterization.py", shell=True)
