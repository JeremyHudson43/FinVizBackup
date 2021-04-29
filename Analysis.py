import pandas as pd

# scan through all folders
folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records\\top gainers\\unique"

df = pd.read_csv("C:\\Users\\Frank Einstein\\Desktop\\stock records\\combined CSVs\\top gainers.csv")

def value_to_float(x):
    if type(x) == float or type(x) == int:
        return x
    if 'K' in x:
        if len(x) > 1:
            return float(x.replace('K', '')) * 1000
        return 1000.0
    if 'M' in x:
        if len(x) > 1:
            return float(x.replace('M', '')) * 1000000
        return 1000000.0
    if 'B' in x:
        return float(x.replace('B', '')) * 1000000000
    return 0.0


market_cap_list = df['Market Cap'].tolist()
market_cap_list = [x for x in market_cap_list if x != '-']

market_cap_sum = 0

for x in market_cap_list:
    x = float(value_to_float(x))
    market_cap_sum +=x

cap_average = market_cap_sum / len(market_cap_list)




outstand_list = df['Shs Outstand'].tolist()
outstand_list = [x for x in outstand_list if x != '-']

outstand_sum = 0

for x in outstand_list:
    print(x)
    x = float(value_to_float(x))
    outstand_sum +=x

outstand_avg = outstand_sum / len(outstand_list)




shares_float_list = df['Shs Float'].tolist()
shares_float_list = [x for x in shares_float_list if x != '-']

shares_float_sum = 0

for x in shares_float_list:
    x = float(value_to_float(x))
    shares_float_sum +=x

float_average = shares_float_sum / len(shares_float_list)




sales_list = df['Sales'].tolist()
sales_list = [x for x in sales_list if x != '-']

sales_sum = 0

for x in sales_list :
    x = float(value_to_float(x))
    sales_sum +=x

sales_average = sales_sum / len(sales_list)



avg_volume_list = df['Avg Volume'].tolist()
avg_volume_list = [x for x in avg_volume_list if x != '-']

avg_volume_sum = 0

for x in avg_volume_list:
    x = float(value_to_float(x))
    avg_volume_sum +=x

average_vol_avg = avg_volume_sum / len(avg_volume_list)


income_list = df['Income'].tolist()
income_list = [x for x in income_list if x != '-']

income_sum = 0

for x in income_list:
    x = float(value_to_float(x))
    income_sum +=x

income_average = income_sum / len(income_list)


df = df.append({'Shs Outstand': outstand_avg, 'Market Cap': cap_average, 'Shs Float': float_average, 'Sales': sales_average, 'Avg Volume': average_vol_avg, 'Income': income_average}, ignore_index=True)


df.to_csv("C:\\Users\\Frank Einstein\\Desktop\\stock records\\combined CSVs\\top gainers.csv")
