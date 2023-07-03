import os

import pandas as pd

BUFFER_PATH = "//192.168.102.50/studyRepository/PBT/analysis/buffer"
#BUFFER_PATH = "data"


def main():
    perts = pd.read_csv("settings/perturbations.csv")

    for sub_folder in os.listdir(BUFFER_PATH, ):
        folder_path = os.path.join(BUFFER_PATH, sub_folder)
        if os.path.isdir(folder_path):
            csv_files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

            if len(csv_files) > 0:
                # Read the first CSV file into a Pandas DataFrame
                csv_file_path = os.path.join(folder_path, csv_files[0])
                cycles = pd.read_csv(csv_file_path)
                perts_cycles_dict = {'perturbation': [],
                                     'cycle_number': []}
                for cycle_number in cycles.index.to_list():
                    start_fm = cycles.loc[cycle_number, "start_frame"]
                    en_fm = cycles.loc[cycle_number, "end_frame"]
                    sub_perts = perts[perts['Subject'] == sub_folder]

                    for perts_id in sub_perts.index.to_list():
                        perts_frame = sub_perts.loc[perts_id, "Frame"]
                        if perts_frame > start_fm and perts_frame < en_fm:
                            side = "Left" if sub_perts.loc[perts_id, "dir"] == 2 else "Right"
                            label = f"{sub_perts.loc[perts_id, 'perturbation']}_{side}"
                            perts_cycles_dict["perturbation"].append(label)
                            perts_cycles_dict["cycle_number"].append(cycle_number)

                cycle_perts = pd.DataFrame(perts_cycles_dict)
                out_file = os.path.join("settings", f"{sub_folder}_perturbation_cycle.csv")
                cycle_perts.to_csv(out_file)


if __name__ == "__main__":
    main()
