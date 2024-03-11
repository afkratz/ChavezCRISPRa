# 00_run_all_scripts.py

import importlib
for file in "01_run_uclust","02_assign_hits_and_clusters","03_charachterize_manual_tested_domains","04_PADDLE_manual_tested_domains":
    print("Running {}".format(file))
    importlib.import_module(file).main()
    print("File {} completed".format(file))

