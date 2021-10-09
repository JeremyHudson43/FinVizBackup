import os
import os.path
import finviz
import pandas as pd
from pandas.tseries.offsets import BDay
import datetime

individual_folder = '5x rel vol'

full_filepath = f"E:\\stock records\\{individual_folder}\\unique"

# full_filepath_two = f"E:\\stock records\\price crossed SMA20\\unique"

# folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records archive\\stock records"

folder_path = "E:\\stock records"

full_filepath = set(os.path.relpath(os.path.join(root, file), full_filepath) for root, _, files in os.walk(full_filepath) for file in files)

# full_filepath_two = set(os.path.relpath(os.path.join(root, file), full_filepath_two) for root, _, files in os.walk(full_filepath_two) for file in files)

# full_filepath = full_filepath & full_filepath_two

full_filepath = full_filepath

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

        being_compared = str(x).split("\\")[2]
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


# good lord this needs cleaned up
def number_of_occurences(stock):
    try:
        count = 0
        stock_list = []
        trends = []
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for filename in [f for f in filenames if f.startswith(stock)]:

                pattern = str(os.path.join(dirpath,filename)).split("\\")[2]
                if pattern not in "all stocks":
                    trends.append(pattern)
                    count +=1

                if len(str(stock)) < 9 and count > 2:
                    stock_list.append(count)
        if len(str(stock)) < 9 and count > 5:

            stock_final = finviz.get_stock(str(stock).replace(".csv", ""))

            # appends new stock data to CSV if it exists, else create CSV
            filepath = "E:\\stock records\\multiple trends\\" + stock

            today = datetime.datetime.today()
            last_business_day = (today - BDay(1)).date()

            stock_final['Date'] = str(last_business_day)
            stock_final['Ticker'] = str(stock).replace(".csv", "")

            try:
                stock_final['News'] = [x[0] for x in finviz.get_news(str(stock).replace(".csv", ""))][0]
            except Exception as e:
                print(e)

            if os.path.isfile(filepath):
                ticker_df = pd.read_csv(filepath, encoding='latin-1', error_bad_lines=False)
                ticker_df = ticker_df.append(stock_final, ignore_index=True)
            else:
                ticker_df = pd.DataFrame(stock_final, index=[0])

            ticker_df = ticker_df.drop_duplicates(subset=['Date'])
            ticker_df.to_csv(filepath, index=False, mode='w+')

            trend_str = ""
            file = open("multiple.txt", "a")
            file.write(str(stock).replace(".csv", "") + " ")
            file.write(str(max(stock_list)) + " ")
            file.write("(")
            for x in range(len(trends)):
                trend_str += trends[x] + ", "
            file.write(trend_str.rstrip(", "))
            file.write(")")
            file.write("\n")
            print(stock, count)
            file.close()

    except Exception as err:
        print()

def multiple():
    for x in listOfFiles:
        number_of_occurences(x.split("\\")[-1])


def cleanup():
    content = open('multiple.txt', 'r')
    sorted_content = set(content.readlines())
    content.close()

    fp = open('multiple.txt', 'w+')

    for line in sorted(sorted_content, key=lambda line: int(line.split()[1])):
        fp.write(line)

    fp.close()

compare()
# multiple()
# cleanup()
