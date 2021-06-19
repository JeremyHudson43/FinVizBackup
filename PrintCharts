import datetime as dt
from datetime import datetime
from datetime import date
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader as web
from dateutil.relativedelta import relativedelta
import os
from os import listdir
from os.path import isfile, join

r = []

# scan through all folders
folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records"

for root, dirs, files in os.walk(folder_path):
    for name in dirs:
        path = os.path.join(root, name)
        r.append(path)

length = (len(next(os.walk(folder_path))[1]))

last_year =  datetime.today() + relativedelta(months=-12)
end = datetime.today()

onlyfiles = []

for x in r[length:]:

    if "unique" in x and "all stocks" not in x:
        onlyfiles = [f for f in listdir(x) if isfile(join(x, f))]

    print(onlyfiles)

    for y in onlyfiles:
        y = y.replace(".csv", "")
        start = last_year.strftime('%Y-%m-%d')
        df = web.get_data_yahoo(y, start, end)
        plt.subplots(figsize=(20, 10))
        df["Adj Close"].plot()
        plt.title(y + " " + str(datetime.today().date()))
        print("Saving to " + y)
        dir = x.replace("unique", "charts")
        plt.savefig(os.path.join(dir, y))
