import subprocess
import os
from pathlib import Path

os.chdir(Path(__file__).resolve().parent)
subprocess.call("python 2_scatterplot.py", shell=True)
subprocess.call("python 2_biochem_auroc.py", shell=True)
subprocess.call("python 2_biochem_distribution.py", shell=True)
subprocess.call("python 2_native_protein_midpoint.py",shell=True)
subprocess.call("python 2_native_protein_start_end.py",shell=True)
subprocess.call("python 2_homolog_families.py",shell=True)

