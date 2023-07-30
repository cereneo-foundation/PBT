import os
import re

from gaitalytics import api, utils

# This is an example pipeline #
###############################

# Define paths
SETTINGS_FILE = "settings/hbm_pig.yaml"
DATA_PATH = "./data/to_analyse"
BUFFER_PATH = "./data/buffer"


def main():
    configs = utils.ConfigProvider(SETTINGS_FILE)
    for root, sub_folder, file_name in os.walk(DATA_PATH):
        r = re.compile(".*\.5\.c3d")
        filtered_files = list(filter(r.match, file_name))
        for filtered_file in filtered_files:
            file_path = f"{root}/{filtered_file}"
            print(file_path)
            subject = filtered_file.replace(".5.c3d", "")
            cycle_path = f"{BUFFER_PATH}/{subject}"
            # read c3d
            if not os.path.exists(cycle_path):
                os.mkdir(cycle_path)
                cycle_data = api.extract_cycles(f"{root}/{filtered_file}", configs, buffer_output_path=cycle_path,
                                                anomaly_checker=[api.GAIT_EVENT_CHECKER_CONTEXT])
            else:
                cycle_data = api.extract_cycles_buffered(cycle_path, configs).get_raw_cycle_points()

            api.normalise_cycles(f"{root}/{filtered_file}", cycle_data, buffer_output_path=cycle_path)



if __name__ == "__main__":
    main()
