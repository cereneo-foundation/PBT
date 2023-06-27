import os
import re
import shutil
from argparse import ArgumentParser, Namespace


# This is an example pipeline #
###############################

# Define paths
SETTINGS_PATH = "settings/"
SETTINGS_FILE = "settings/hbm_pig.yaml"
#DATA_PATH = "//192.168.102.50/studyRepository/PBT/vicon/"
DATA_PATH = "C:\\ViconData\\PBT\\Test_1\\"

def main():
    for root, sub_folder, file_name in os.walk(DATA_PATH, topdown=False):
        r = re.compile(".*\.2\.c3d")
        filtered_files = list(filter(r.match, file_name))
        for filtered_file in filtered_files:
            print(f"{root}/{filtered_file}")

            filtered_copy = filtered_file.replace("2.c3d", "3.c3d")
            if not os.path.exists(f"{root}/{filtered_copy}"):
                shutil.copyfile(f"{root}/{filtered_file}", f"{root}/{filtered_copy}")




# Using the special variable
# __name__
if __name__ == "__main__":
    main()
