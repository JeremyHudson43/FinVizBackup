# scan through all folders
import pandas as pd
import os
import datetime
from pandas.tseries.offsets import BDay

folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records"

r = []

today = datetime.datetime.today()
last_business_day = (today - BDay(1)).date()

weekno = datetime.datetime.today().weekday()

if 6 > weekno > 0:

    for root, dirs, files in os.walk(folder_path):
        for name in dirs:
            path = os.path.join(root, name)
            r.append(path)

    for x in r[24:]:

        path = x.replace("unique", "")

        check_path = os.path.join(path, str(last_business_day) + ".csv")

        if os.path.isfile(check_path):

            df = (pd.read_csv(os.path.join(path, str(last_business_day) + ".csv")))

            for index, row in df.iterrows():

                ticker = row['Ticker']

                with open(r"C:\Users\Frank Einstein\Desktop\long term records\list of tickers.txt", "a+") as myfile:

                        if not(ticker in myfile.readlines()):
                            myfile.writelines(ticker + '\n')

                            tickers = myfile.readlines()

                        myfile.close()