import pandas as pd
import glob
import os

# scan through all folders
folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\top gainers\\unique"

df = pd.concat(map(pd.read_csv, glob.glob(os.path.join(folder_path, "*.csv"))))

df['Market Cap'] = (df['Market Cap'].replace(r'[KMB]+$', '', regex=True).astype(float) *
              df['Market Cap'].str.extract(r'[\d\.]+([KMB]+)', expand=False)
               .fillna(1)
                .replace(['K','M', 'B'], [10**3, 10**6, 10**9]).astype(int))

print(df["Market Cap"].mean())