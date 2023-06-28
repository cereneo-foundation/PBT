import os
import re
from argparse import ArgumentParser, Namespace

from gaitalytics import utils, c3d, modelling
import pandas as pd

# This is an example pipeline #
###############################

# Define paths
SETTINGS_FILE = "settings/hbm_pig.yaml"
DATA_PATH = "//192.168.102.50/studyRepository/PBT/vicon"
# DATA_PATH = "./data"
out_path = "./test/data/Baseline.5.c3d"

def main():
    configs = utils.ConfigProvider(SETTINGS_FILE)

    #read speeds file
    speeds = pd.read_csv("speed.csv", delimiter=";")
    speeds = speeds.set_index("subject")

    for root, sub_folder, file_name in os.walk(DATA_PATH):
        r = re.compile(".*\.4\.c3d")
        filtered_files = list(filter(r.match, file_name))
        for filtered_file in filtered_files:

            file_path = f"{root}/{filtered_file}"
            print(file_path)
            # read c3d
            acq_trial = c3d.read_btk(file_path)


            # calculate com
            com_modeller = modelling.COMModeller(configs)
            com_modeller.create_point(acq_trial)

            # get belt speed
            subject = utils.extract_subject(acq_trial)
            if subject.subject in speeds.index.values:
                belt_speed = speeds.loc[subject.subject]["speed"]

                # Margin of stability left cycles
                left_cmos_modeller = modelling.CMoSModeller("Left", configs, subject.left_leg_length, belt_speed)
                left_cmos_modeller.create_point(acq_trial)

                # Margin of stability right cycles
                right_cmos_modeller = modelling.CMoSModeller("Right", configs, subject.right_leg_length, belt_speed)
                right_cmos_modeller.create_point(acq_trial)

                filtered_copy = filtered_file.replace("4.c3d", "5.c3d")
                c3d.write_btk(acq_trial, f"{root}/{filtered_copy}")
            else:
                print("Subject not in speeds file")

# Using the special variable
# __name__
if __name__ == "__main__":
    main()
