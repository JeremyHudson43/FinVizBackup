import os
import shutil

folder_path = r"C:\Users\Frank Einstein\Desktop\stock records\all stocks\unique"
long_term_path = r"C:\Users\Frank Einstein\Desktop\long term records"

src_files = os.listdir(folder_path)
for file_name in src_files:
    full_file_name = os.path.join(folder_path, file_name)
    if os.path.isfile(full_file_name):
        shutil.copy(full_file_name, long_term_path)



