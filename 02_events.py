import os
import re
from argparse import ArgumentParser, Namespace

from gaitalytics import utils, api

# This is an example pipeline #
###############################

# Define paths
SETTINGS_FILE = "settings/hbm_pig.yaml"
#DATA_PATH = "//192.168.102.50/studyRepository/PBT/vicon"
DATA_PATH = "C:\\ViconData\\PBT\\Test_1\\"

def main():
    configs = utils.ConfigProvider(SETTINGS_FILE)
    for root, sub_folder, file_name in os.walk(DATA_PATH):
        r = re.compile(".*\.3\.c3d")
        filtered_files = list(filter(r.match, file_name))
        for filtered_file in filtered_files:
            file_path = f"{root}/{filtered_file}"
            print(file_path)
            api.detect_gait_events(file_path, root, configs)




# Using the special variable
# __name__
if __name__ == "__main__":
    main()
