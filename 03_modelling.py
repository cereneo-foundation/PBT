import os
import re

import pandas as pd
from gaitalytics import c3d, api, utils

# This is an example pipeline #
###############################

# Define paths
SETTINGS_FILE = "settings/hbm_pig.yaml"
TREADMILL_SPEED_FILE = "settings/speed.csv"
DATA_PATH = "//192.168.102.50/studyRepository/PBT/vicon"
#DATA_PATH = "./data"


def main():
    configs = utils.ConfigProvider(SETTINGS_FILE)

    # read speeds file
    speeds = pd.read_csv(TREADMILL_SPEED_FILE)
    speeds = speeds.set_index("Subject")

    for root, sub_folder, file_name in os.walk(DATA_PATH):
        r = re.compile(".*\.4\.c3d")
        filtered_files = list(filter(r.match, file_name))
        for filtered_file in filtered_files:

            file_path = f"{root}/{filtered_file}"
            print(file_path)
            # read c3d
            acq_trial = c3d.read_btk(file_path)

            # get belt speed
            subject = utils.extract_subject(acq_trial)
            if subject.subject in speeds.index.values:
                belt_speed = float(speeds.loc[subject.subject]["speed"])
                api.model_data(f"{root}/{filtered_file}", DATA_PATH, configs, api.MODELLING_CMOS, belt_speed=belt_speed)
            else:
                print("Subject not in speeds file")


# Using the special variable
# __name__
if __name__ == "__main__":
    main()
