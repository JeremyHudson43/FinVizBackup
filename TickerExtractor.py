import pandas as pd
import os

# scan through all folders
folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\analysts buy"
unique = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\analysts buy\\unique"

for filename in os.listdir(folder_path):

    if filename.endswith(".csv"):

        df = pd.read_csv(os.path.join(folder_path, filename))

        for index, row in df.iterrows():

            ticker = row['Ticker']

            only_ticker = df[df['Ticker'] == ticker]

            filepath = os.path.join(unique, (ticker + ".csv"))

            only_ticker.drop(only_ticker.columns[1], axis=1, inplace=True)

            only_ticker.to_csv(filepath, sep=',', header=None, mode='a+')
