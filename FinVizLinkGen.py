import os

file_str = ""
base_link = "https://finviz.com/screener.ashx?t="

folder_name = "price crossed SMA50/unique"

for root, dirs, files in os.walk("C:\\Users\\Frank Einstein\\Desktop\\stock records\\" + folder_name):
    for file in files:
        if file.endswith(".csv"):
             file = file.replace(".csv", "")
             file_str += file +","

link = base_link + file_str[:-1]

file = open("C:\\Users\\Frank Einstein\\Desktop\\stock records\\" + folder_name + "\\finviz.txt", "w+")
file.write(link.replace("-", "") + "\n")
file.close()