import pandas as pd
import os
import pickle
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(script_dir, "[3 data] complete_dataframes.pkl"), "rb") as f:
    complete_dataframes = pickle.load(f)

# Add an 'Study' column to each dataframe before concatenation. We need this as the random effects term in the model.
dfs_with_origin = []
for key, df in complete_dataframes.items():
    df_copy = df.copy()
    df_copy['Study'] = key
    dfs_with_origin.append(df_copy)

merged_df = pd.concat(dfs_with_origin, axis=0, ignore_index=True, sort=False)

merged_df = merged_df.loc[:, ~merged_df.columns.str.contains("Unnamed")]

merged_csv_path = os.path.join(script_dir, "[4 data] prepared_for_liwc.csv")
merged_df.to_csv(merged_csv_path, index=False)

