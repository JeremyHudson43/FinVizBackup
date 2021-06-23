import os
import os.path

individual_folder = 'analysts buy'

full_filepath = f"C:\\Users\\Frank Einstein\\Desktop\\stock records archive\\stock records\\{individual_folder}\\unique"

folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records archive\\stock records"

# full_filepath = f"C:\\Users\\Frank Einstein\\Desktop\\stock records\\{individual_folder}\\unique"

# folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records"


full_filepath = set(os.path.relpath(os.path.join(root, file), full_filepath) for root, _, files in os.walk(full_filepath) for file in files)

file_list = []

for root, dirs, files in os.walk(folder_path):
    for name in dirs:
        path = os.path.join(root, name)
        file_list.append(path)

length = (len(next(os.walk(folder_path))[1]))


def compare():
    for x in file_list[length:]:
        compare = set(os.path.relpath(os.path.join(root, file), x) for root, _, files in os.walk(x) for file in files)

        # being_compared = str(x).split("\\")[6]

        being_compared = str(x).split("\\")[5]
        being_compared_length = str(len(compare))

        common_stocks_length = str(len(compare & full_filepath))
        base_comparison_length = (len(full_filepath))

        percentage_similarity = len(compare & full_filepath) / (len(full_filepath)) * 100
        percentage_similarity = "{:.2f}".format(percentage_similarity)

        print(f"Current length of {individual_folder} is {base_comparison_length}")

        print(f"Current length of {being_compared} is {being_compared_length}\n")

        print(f"Number of common stocks between {being_compared} and {individual_folder} is {common_stocks_length}\n")

        print(f"The common stocks in {individual_folder} and {being_compared} are\n{compare & full_filepath}")

        try:
            print(f"\n{being_compared} contains {percentage_similarity}% of the stocks in {individual_folder}\n")
        except Exception as err:
            print(err)

# compare()
listOfFiles = []


for (dirpath, dirnames, filenames) in os.walk(folder_path):
    listOfFiles += [os.path.join(dirpath, file) for file in filenames]


def number_of_occurences(stock):
    try:
        count = 0
        stock_list = []
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in [f for f in filenames if f.startswith(stock)]:
                count +=1

                if len(str(stock)) < 9 and count > 8:
                    stock_list.append(count)
        if len(str(stock)) < 9 and count > 8:
            file = open("multiple.txt", "a")
            file.write(str(stock) + " ")
            file.write(" " + str(max(stock_list)))
            file.write("\n")
            print(stock, count)
            file.close()

    except Exception as err:
        print()

def multiple():
    for x in listOfFiles:
        number_of_occurences(x.split("\\")[-1])


multiple()
content = open("multiple.txt", 'r').readlines()
content_set = set(content)
clean_data = open("multiple.txt", 'w')

for line in content_set:
    clean_data.write(line)
