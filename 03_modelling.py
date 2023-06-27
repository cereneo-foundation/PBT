import os
import re
from argparse import ArgumentParser, Namespace

from gaitalytics import utils, c3d, modelling

# This is an example pipeline #
###############################

# Define paths
SETTINGS_FILE = "settings/hbm_pig.yaml"
DATA_PATH = "//192.168.102.50/studyRepository/PBT/vicon"
out_path = "./test/data/Baseline.5.c3d"

def main():
    configs = utils.ConfigProvider(SETTINGS_FILE)
    for root, sub_folder, file_name in os.walk(DATA_PATH):
        r = re.compile(".*\.4\.c3d")
        filtered_files = list(filter(r.match, file_name))
        for filtered_file in filtered_files:
            file_path = f"{root}/{filtered_file}"
            print(file_path)
            # read c3d
            acq_trial = c3d.read_btk(file_path)
            com_modeller = modelling.COMModeller(configs)
            com_modeller.create_point(acq_trial)
            #cmos_modeller = modelling.MLcMoSModeller(configs, 100, 1.3)
            #cmos_modeller.create_point(acq_trial)
            filtered_copy = filtered_file.replace("4.c3d", "5.c3d")
            c3d.write_btk(acq_trial, f"{root}/{filtered_copy}")

# Using the special variable
# __name__
if __name__ == "__main__":
    main()
