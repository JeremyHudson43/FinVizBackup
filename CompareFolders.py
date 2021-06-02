import os

top_gainers = r"C:\Users\Frank Einstein\Desktop\stock records\top gainers averages\unique"
folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records"

# top_gainers = r"C:\Users\Frank Einstein\Desktop\stock records old\stock records\top gainers\unique"
# folder_path = r"C:\Users\Frank Einstein\Desktop\stock records old\stock records"


top_gainers = set(os.path.relpath(os.path.join(root, file), top_gainers) for root, _, files in os.walk(top_gainers) for file in files)

r = []

for root, dirs, files in os.walk(folder_path):
    for name in dirs:
        path = os.path.join(root, name)
        r.append(path)

for x in r[33:]:
    compare = set(os.path.relpath(os.path.join(root, file), x) for root, _, files in os.walk(x) for file in files)

    print("Number of common stocks between " + str(x).split("\\")[5]
    + " and the top gainers is " + str(len(compare & top_gainers)))

    print("\n")

    print("Current length of top gainers is " + str(len(top_gainers)))
    print("Current length of " + str(x).split("\\")[5] + " is " + str(len(compare)))

    print("\n")
    print("The common stocks in " + str(x).split("\\")[5] + " and the top gainers are")

    print("\n")
    print(compare & top_gainers)
    print("\n")

    try:
        print(str(x).split("\\")[5] + " contains " + str(len(compare & top_gainers) / (len(top_gainers)) * 100) + "%" + " of the stocks in top gainers")
    except:
        print("error")

    print("\n")






