import pandas as pd
import os
import pickle
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(script_dir, "[1 data] data_frame_groups.pkl"), "rb") as f:
    data_frame_groups = pickle.load(f)

averaged_dataframes = {}
for filename, dfs in data_frame_groups.items():
    # Align to ensure same index and columns
    aligned = [df.reindex_like(dfs[0]) for df in dfs]

    numeric_cols = dfs[0].select_dtypes(include=[np.number]).columns
    non_numeric_cols = dfs[0].columns.difference(numeric_cols)

    # Average numeric columns
    stacked = np.stack([df[numeric_cols].values for df in aligned])
    avg = np.nanmean(stacked, axis=0)
    avg_df = pd.DataFrame(avg, columns=numeric_cols, index=dfs[0].index)
    
    for col in non_numeric_cols:
        avg_df[col] = dfs[0][col]

    # Reorder columns to match original
    avg_df = avg_df[dfs[0].columns]
    averaged_dataframes[filename] = avg_df

with open(os.path.join(script_dir, "[2 data] averaged_dataframes.pkl"), "wb") as f:
    pickle.dump(averaged_dataframes, f)