import os
import re
from argparse import ArgumentParser, Namespace

from gaitalytics import utils, c3d, events

# This is an example pipeline #
###############################

# Define paths
SETTINGS_FILE = "settings/hbm_pig.yaml"
#DATA_PATH = "//192.168.102.50/studyRepository/PBT/vicon"
DATA_PATH = "./data/events_cleaned"

def main():
    for root, sub_folder, file_name in os.walk(DATA_PATH):
        r = re.compile(".*\.4\.c3d")
        filtered_files = list(filter(r.match, file_name))
        for filtered_file in filtered_files:
            file_path = f"{root}/{filtered_file}"
            print(file_path)
            acq_trial = c3d.read_btk(f"{root}/{filtered_file}")
            detected, anomalies = events.ContextPatternChecker().check_events(acq_trial)
            if detected:
                print(f"detected")
                event_anomaly = filtered_file.replace(".4.c3d", "_anomalies.txt")
                f = open(f"{root}/{event_anomaly}", "w")
                for anomaly in anomalies:
                    print(anomaly,file=f)

                f.close()





# Using the special variable
# __name__
if __name__ == "__main__":
    main()
