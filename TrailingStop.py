import pandas as pd

individual_folder = 'small cap rel vol'
stock_name = "CBAN" + ".csv"


# folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\small cap rel vol\\unique\\"
folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\" + individual_folder + "\\unique\\"
storage_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\combined CSVs\\"

df = pd.read_csv(folder_path + stock_name)

df = pd.DataFrame(['Price'])
df['highest'] = df.cummax()

df['trailingstop'] = df['highest'] * 0.99
df['exit_signal'] = df['price'] < df['trailingstop']

print(df.head())