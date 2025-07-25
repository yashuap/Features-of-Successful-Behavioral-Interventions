import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

cleaned_path = os.path.join(script_dir, "[5 data] post_liwc.csv")
df = pd.read_csv(cleaned_path)
liwc_vars = ["WC", "emo_pos", "emo_neg", "moral", "prosocial", "conflict", "power", "politic", "tech", "relig", "health", "reward", "risk"]

# Some DVs need to be reverse-coded
df["Percentage Increase (Partisan Animosity)"] = -df["Percentage Increase (Partisan Animosity)"]
df["Percentage Increase (Undemocratic Practices)"] = -df["Percentage Increase (Undemocratic Practices)"]
df['Percentage Increase (Gym Visits)'] = df['Change in Total Weekly Gym Visits']/1.5 * 100 # 1.5 was control

# Misnamed column, so we rename it
df["Percentage Increase (COVID Booster Uptake)"] = df["Increase in COVID Booster Uptake (30 days) (beta)"]

df["Percentage Increase (Collective Blame)"] = -df["Percentage Increase (Collective Blame)"]
df["Percentage Increase (Blatant Dehumanization)"] = -df["Percentage Increase (Blatant Dehumanization)"]
df["Percentage Increase (Prejudice)"] = -df["Percentage Increase (Prejudice)"]
df["Percentage Increase (Punitive Counterterrorism)"] = -df["Percentage Increase (Punitive Counterterrorism)"]
df["Percentage Increase (Anti-Muslim Policy Support)"] = -df["Percentage Increase (Anti-Muslim Policy Support)"]

specificity_cols = [col for col in df.columns if "Specificity" in str(col)]
dv_cols = [col for col in df.columns if "Percentage Increase" in str(col)]

for var in ["Text"]:
    df[var] = df[var].astype("bool")

df["Dominant Modality"] = df["Dominant Modality"].astype("category")

id_vars = ["Study", "Intervention", "Text", "Video", "Image", "Audio", "Open-ended", "Close-ended", "Dominant Modality", "Engagement"]
id_vars = id_vars + liwc_vars

df_melted = pd.melt(df, id_vars=id_vars, value_vars=specificity_cols+dv_cols, var_name="var", value_name="value")
df_melted[['var_type', 'DV']] = df_melted['var'].str.extract(r'(Specificity|Percentage Increase) \(([^)]+)\)')
df_melted = df_melted.dropna(subset=['value'])

df_final = df_melted.pivot(index=id_vars+['DV'], columns='var_type', values='value').reset_index()

# If formated as X%, convert to X. 
# In order to interpret the result as "This feature results in an X% increase to the DV", we do not divide by 100.
def percentage_to_float(x):
    if isinstance(x, str):
        return float(x[:-1])
    else:
        return x

df_final["Percentage Increase"] = df_final["Percentage Increase"].apply(percentage_to_float)

# Remove special characters
df_final = df_final.rename(columns={
    'Percentage Increase': 'Increase', 
    "Intervention Name": "Intervention",
    "Dominant Modality": "Modality",
    "Open-ended": "OpenEnded",
    "Close-ended": "CloseEnded",
})

df_final["Specificity"] = df_final["Specificity"].astype('float64')
df_final["bVideo"] = df_final["Video"] > 0
df_final["bImage"] = df_final["Image"] > 0


final_path = os.path.join(script_dir, "[data] final.csv")
df_final.to_csv(final_path, index=False)