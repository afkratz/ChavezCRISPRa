# 2_all_panels.py

import subprocess
import os
from pathlib import Path

os.chdir(Path(__file__).resolve().parent)


def run_script(script_name):
    try:
        subprocess.run(["python", script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {script_name}: {e}")

if __name__ == "__main__":
    # List of scripts to be executed in order
    scripts_to_run = [
        "2abc3sde_biochem_hits_v_misses.py",
        "2d_native_protein_start_end.py",
        "2e_native_protein_midpoint.py",
        "2sa_scatterplot.py",
        "2sb_homolog_families.py",
        "3sa_biochem_distribution.py",
        ]

    for script in scripts_to_run:
        run_script(script)
