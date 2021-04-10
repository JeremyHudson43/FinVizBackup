import pandas as pd
import os
import glob

# scan through all folders
folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\analysts buy"
unique = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\analysts buy\\unique"

all_files = glob.glob(os.path.join(folder_path, "*.csv"))

df = (pd.read_csv(f) for f in all_files)
df = pd.concat(df, ignore_index=True)

for index, row in df.iterrows():

    ticker = row['Ticker']

    only_ticker = df[df['Ticker'] == ticker]

    filepath = os.path.join(unique, (ticker + ".csv"))

    only_ticker.to_csv(filepath)


