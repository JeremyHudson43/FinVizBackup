import os.path
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join

# scan through all folders
folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\combined CSVs"

file_list = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]

length = (len(next(os.walk(folder_path))[1]))

# extract tickers from scraped mass CSVs to generate individual stock CSVs
for unique_path in file_list[length:]:

    print(unique_path)

    if "all_filtered" in unique_path:

        df = pd.read_csv(os.path.join(folder_path, unique_path))
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        corr = df.corr()

        plt.subplots(figsize=(80, 60))

        ax = sns.heatmap(
            corr,
            vmin=-1, vmax=1, center=0,
            cmap=sns.diverging_palette(20, 220, n=200),
            square=True,
            annot=True
        )

        ax.set_xticklabels(
            ax.get_xticklabels(),
            rotation=45,
            horizontalalignment='right'
        );

        to_save = unique_path.split("\\")[-1][:-4]

        print(to_save)

        plt.savefig(f"C:\\Users\\Frank Einstein\\Desktop\\heatmaps\\{to_save}")
