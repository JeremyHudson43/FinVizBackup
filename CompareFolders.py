import os

# top_gainers = r"C:\Users\Frank Einstein\Desktop\stock records\top gainers\unique"
# folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records"

top_gainers = r"C:\Users\Frank Einstein\Desktop\stock records old\stock records\top gainers\unique"
folder_path = r"C:\Users\Frank Einstein\Desktop\stock records old\stock records"


top_gainers = set(os.path.relpath(os.path.join(root, file), top_gainers ) for root, _, files in os.walk(top_gainers) for file in files)

r = []

for root, dirs, files in os.walk(folder_path):
    for name in dirs:
        path = os.path.join(root, name)
        r.append(path)

for x in r[28:]:
    if "top gainers" not in x:
        compare = set(os.path.relpath(os.path.join(root, file), x) for root, _, files in os.walk(x) for file in files)
        print("The common stocks in " + str(x).split("\\")[6] + " and the top gainers are")
        print(compare & top_gainers)
        print("\n")





