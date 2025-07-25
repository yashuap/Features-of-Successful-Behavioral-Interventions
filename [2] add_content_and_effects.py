import pandas as pd
import os
import pickle
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(script_dir, "[2 data] averaged_dataframes.pkl"), "rb") as f:
    averaged_dataframes = pickle.load(f)

content_dir = os.path.join(script_dir, "[2 data] content")
effects_dir = os.path.join(script_dir, "[2 data] effects")

complete_dataframes = {}

for filename, df in averaged_dataframes.items():
    content_path = os.path.join(content_dir, filename)
    effects_path = os.path.join(effects_dir, filename)
    
    df_aug = df.copy()
    
    # Merge content columns
    if os.path.exists(content_path):
        content_df = pd.read_excel(content_path)
        content_df = content_df.loc[:, ~content_df.columns.str.contains("Link", case=False)]
        
        df_aug = df_aug.merge(content_df, on="Intervention", how="left", suffixes=('', '_content'))
        
        # Reorder columns to place content columns after 'Intervention'
        cols = list(df_aug.columns)
        if "Intervention" in cols:
            intervention_idx = cols.index("Intervention")
            
            content_cols = [col for col in content_df.columns if col != "Intervention" and col in df_aug.columns]
            
            for col in content_cols:
                cols.remove(col)
            
            for i, col in enumerate(content_cols):
                cols.insert(intervention_idx + 1 + i, col)
            df_aug = df_aug[cols]
    
    # Merge effects columns
    if os.path.exists(effects_path):
        effects_df = pd.read_excel(effects_path)
        
        effects_df = effects_df.loc[:, ~effects_df.columns.str.contains("Link", case=False)]
        
        df_aug = df_aug.merge(effects_df, on="Intervention", how="left", suffixes=('', '_effects'))
    
    complete_dataframes[filename] = df_aug


with open(os.path.join(script_dir, "[3 data] complete_dataframes.pkl"), "wb") as f:
    pickle.dump(complete_dataframes, f)

