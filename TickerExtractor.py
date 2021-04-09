import pandas as pd
import os
from csv import writer
import re

# scan through all folders
folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\analysts buy"
unique = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\analysts buy\\unique"

for filename in os.listdir(folder_path):

    if filename.endswith(".csv"):

        df = pd.read_csv(os.path.join(folder_path, filename))

        for index, row in df.iterrows():

            ticker = row['Ticker']

            only_ticker = df[df['Ticker'] == ticker]

            header = pd.DataFrame()

            filepath = os.path.join(unique, (ticker + ".csv"))

            only_ticker.drop(only_ticker.columns[1], axis=1, inplace=True)

            List = only_ticker.values.tolist()

            str_List = str(List)

            split = str_List.split()

            new_split = []

            if(not(os.path.isfile(filepath))):

                # Open our existing CSV file in append mode
                # Create a file object for this file
                with open(filepath, 'a') as f_object:

                    header = ['Perf Week', 'Perf Month', 'Perf Quart', 'Perf Half',
                              'Perf Year', 'Perf YTD', 'Volatility W', 'Volatility M',
                              'Recom', 'Avg Volume', 'Rel Volume', 'Price', 'Change',
                              'Volume']

                    writer_object = writer(f_object)
                    writer_object.writerow(header)

            elif(os.path.isfile(filepath)):

                # Open our existing CSV file in append mode
                # Create a file object for this file
                with open(filepath, 'a') as f_object:

                    writer_object = writer(f_object)

                    # Pass the list as an argument into
                    # the writerow()

                    for x in split:
                        x = x.replace("'", "")
                        x = x.replace("[", "")
                        x = x.replace("]", "")
                        x = x.replace(",", "")
                        new_split.append(x)

                    new_split.pop(0)

                    writer_object.writerow(new_split)

                    # Close the file object
                    f_object.close()
