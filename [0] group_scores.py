import pandas as pd
import os
import pickle

script_dir = os.path.dirname(os.path.abspath(__file__))

scores_dir = os.path.join(script_dir, "[0 data] scores")
shared_files = {}

for subdir in os.listdir(scores_dir):
    subdir_path = os.path.join(scores_dir, subdir)
    if os.path.isdir(subdir_path):
        for filename in os.listdir(subdir_path):
            if filename == ".DS_Store":
                continue  
            file_path = os.path.join(subdir_path, filename)
            if os.path.isfile(file_path):
                if filename not in shared_files:
                    shared_files[filename] = set()
                rel_path = os.path.relpath(file_path, script_dir)
                shared_files[filename].add(rel_path)

# Create a dictionary: key = filename, value = list of dataframes
data_frame_groups = {}
for filename, paths in shared_files.items():
    if len(paths) > 1:
        dfs = [pd.read_excel(os.path.join(script_dir, fp)) for fp in paths]
        data_frame_groups[filename] = dfs

with open(os.path.join(script_dir, "[1 data] data_frame_groups.pkl"), "wb") as f:
    pickle.dump(data_frame_groups, f)