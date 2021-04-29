import pandas as pd
import glob
import functools


individual_folder = 'top gainers'

# folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\small cap rel vol\\unique\\"
folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records old\\stock records\\" + individual_folder + "\\unique\\"
storage_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\combined CSVs\\"

df = pd.concat(map(functools.partial(pd.read_csv, encoding='latin-1', compression=None),
                    glob.glob(folder_path + "/*.csv")))

df.to_csv(storage_path + individual_folder + ".csv")