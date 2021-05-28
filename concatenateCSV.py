import pandas as pd
import glob
import functools


individual_folder = r'C:\Users\Frank Einstein\Desktop\stock records\potential uptrend from lows'

# folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\small cap rel vol\\unique\\"

folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records old\\stock records\\" + individual_folder + "\\unique\\"

folder_path = r"C:\Users\Frank Einstein\Desktop\long term records"

storage_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\combined CSVs\\"

df = pd.concat(map(functools.partial(pd.read_csv, encoding='latin-1', compression=None,  error_bad_lines=False),
                    glob.glob(folder_path + "/*.csv")))

df.to_csv(storage_path + "all_combined" + ".csv", index=False)