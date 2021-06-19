from finviz.screener import Screener
import os
import datetime
import pandas as pd
# BDay is business day, not birthday...
from pandas.tseries.offsets import BDay
import time

today = datetime.datetime.today()
last_business_day = (today - BDay(1)).date()

folder_path = "C:\\Users\\Frank Einstein\\Desktop\\stock records"

def small_mc_rel_vol():
    # small market cap stocks with few shares outstanding
    filters = ['cap_microunder','sh_float_u10','sh_outstanding_u10','sh_price_u15','sh_relvol_o2']
    stock_list = Screener(filters=filters, table='Performance', order='price')

    # Export the screener results to .csv
    stock_list.to_csv(os.path.join(folder_path, ("small cap rel vol\\" + str(last_business_day) + ".csv")))

def analysts_buy():
    filters = ['an_recom_strongbuy','sh_price_u5','targetprice_a50']
    stock_list = Screener(filters=filters, table='Performance', order='Recom')

    path = os.path.join(folder_path, ("analysts buy\\" + str(last_business_day) + ".csv"))

    my_df = pd.DataFrame(stock_list[0:200])

    my_df.to_csv(path, index=False, mode='w', header=['No.','Ticker', 'Perf Week', 'Perf Month', 'Perf Quart', 'Perf Half',
                              'Perf Year', 'Perf YTD', 'Volatility W', 'Volatility M',
                              'Recom', 'Avg Volume', 'Rel Volume', 'Price', 'Change',
                              'Volume'])


def bankruptcy_squeeze_candidates():
    # small market cap stocks with few shares outstanding
    filters = ['fa_pb_low','sh_short_o30']
    stock_list = Screener(filters=filters, table='Performance', order='price')

    # Export the screener results to .csv
    stock_list.to_csv(os.path.join(folder_path, ("bankruptcy squeeze candidates\\" + str(last_business_day) + ".csv")))


def bounce_at_moving_average():
    # small market cap stocks with few shares outstanding
    filters = ['sh_avgvol_o400','sh_curvol_o2000','sh_relvol_o1','ta_sma20_pa','ta_sma50_pb']
    stock_list = Screener(filters=filters, table='Performance', order='price')

    # Export the screener results to .csv
    stock_list.to_csv(os.path.join(folder_path, ("bounce at moving average\\" + str(last_business_day) + ".csv")))


def breaking_out():
    # small market cap stocks with few shares outstanding
    filters = ['fa_debteq_u1','fa_roe_o20','sh_avgvol_o100','ta_highlow50d_nh','ta_sma20_pa','ta_sma200_pa','ta_sma50_pa']
    stock_list = Screener(filters=filters, table='Performance', order='price')

    # Export the screener results to .csv
    stock_list.to_csv(os.path.join(folder_path, ("breaking out\\" + str(last_business_day) + ".csv")))


def buy_and_hold_value():
    # small market cap stocks with few shares outstanding
    filters = ['cap_microover','fa_curratio_o1.5','fa_estltgrowth_o10','fa_peg_o1','fa_roe_o15','ta_beta_o1.5','ta_sma20_pa']
    stock_list = Screener(filters=filters, table='Performance', order='price')

    # Export the screener results to .csv
    stock_list.to_csv(os.path.join(folder_path, ("buy and hold value\\" + str(last_business_day) + ".csv")))


def canslim():
    # small market cap stocks with few shares outstanding
    filters = ['fa_eps5years_o20','fa_epsqoq_o20','fa_epsyoy_o20','fa_sales5years_o20','fa_salesqoq_o20','sh_curvol_o200']
    stock_list = Screener(filters=filters, table='Performance', order='price')

    # Export the screener results to .csv
    stock_list.to_csv(os.path.join(folder_path, ("canslim\\" + str(last_business_day) + ".csv")))


def consistent_growth_bullish_trend():
    # small market cap stocks with few shares outstanding

    filters = ['fa_eps5years_pos','fa_epsqoq_o20','fa_epsyoy_o25','fa_epsyoy1_o15','fa_estltgrowth_pos',
               'fa_roe_o15','sh_instown_o10','sh_price_o15','ta_highlow52w_a90h','ta_rsi_nos50']

    stock_list = Screener(filters=filters, table='Performance', order='price')

    # Export the screener results to .csv
    stock_list.to_csv(os.path.join(folder_path, ("consistent growth bullish trend\\" + str(last_business_day) + ".csv")))


def earnings_gap_up():
    # small market cap stocks with few shares outstanding
    filters = ['earningsdate_tomorrowafter','sh_avgvol_o400','sh_curvol_o50','sh_short_u25','ta_averagetruerange_o0.5','ta_gap_u2']
    stock_list = Screener(filters=filters, table='Performance', order='price')

    # Export the screener results to .csv
    stock_list.to_csv(os.path.join(folder_path, ("earnings gap up\\" + str(last_business_day) + ".csv")))


def high_earnings_growth():
    # small market cap stocks with few shares outstanding
    filters = ['fa_epsqoq_o25','fa_epsyoy_o25','fa_epsyoy1_o25','fa_salesqoq_o25','sh_avgvol_o400','ta_rsi_nos50','ta_sma200_pa']
    stock_list = Screener(filters=filters, table='Performance', order='price')

    # Export the screener results to .csv
    stock_list.to_csv(os.path.join(folder_path, ("high earnings growth\\" + str(last_business_day) + ".csv")))


def high_relative_volume():
    # small market cap stocks with few shares outstanding
    filters = ['fa_curratio_o1','fa_epsqoq_o15','fa_quickratio_o1','fa_salesqoq_o15','sh_avgvol_o400','sh_price_o5',
               'sh_relvol_o1.5','ta_sma20_pa','ta_sma200_sb50','ta_sma50_sa200']
    stock_list = Screener(filters=filters, table='Performance', order='price')

    # Export the screener results to .csv
    stock_list.to_csv(os.path.join(folder_path, ("high relative volume\\" + str(last_business_day) + ".csv")))


def high_sales_growth():
    # small market cap stocks with few shares outstanding
    filters = ['fa_debteq_u0.5','fa_roe_o15','fa_sales5years_o20','fa_salesqoq_o20','sh_avgvol_o200','sh_instown_o60','sh_price_o5','sh_short_u5']
    stock_list = Screener(filters=filters, table='Performance', order='price')

    # Export the screener results to .csv
    stock_list.to_csv(os.path.join(folder_path, ("high sales growth\\" + str(last_business_day) + ".csv")))


def low_pe_value():
    # small market cap stocks with few shares outstanding
    filters = ['cap_smallunder','fa_pb_low','fa_pe_low,fa_peg_low','fa_roa_pos','fa_roe_pos','sh_price_o5']
    stock_list = Screener(filters=filters, table='Performance', order='price')

    # Export the screener results to .csv
    stock_list.to_csv(os.path.join(folder_path, ("low pe value\\" + str(last_business_day) + ".csv")))


def new_highs():
    # small market cap stocks with few shares outstanding
    filters = ['an_recom_buy','sh_price_u7','ta_change_u','ta_highlow20d_nh','ta_highlow50d_nh','ta_highlow52w_nh','ta_perf_dup']
    stock_list = Screener(filters=filters, table='Performance', order='price')

    # Export the screener results to .csv
    stock_list.to_csv(os.path.join(folder_path, ("new highs\\" + str(last_business_day) + ".csv")))


def oversold_reversal():
    # small market cap stocks with few shares outstanding
    filters = ['sh_price_o5','sh_relvol_o2','ta_change_u','ta_rsi_os30']
    stock_list = Screener(filters=filters, table='Performance', order='price')

    # Export the screener results to .csv
    stock_list.to_csv(os.path.join(folder_path, ("oversold reversal\\" + str(last_business_day) + ".csv")))


def oversold_upcoming_earnings():
    # small market cap stocks with few shares outstanding
    filters = ['cap_smallover','earningsdate_thismonth','fa_epsqoq_o15','fa_grossmargin_o20','sh_avgvol_o750','sh_curvol_o1000','ta_perf_52w10o','ta_rsi_nob50']
    stock_list = Screener(filters=filters, table='Performance', order='price')

    # Export the screener results to .csv
    stock_list.to_csv(os.path.join(folder_path, ("oversold upcoming earnings\\" + str(last_business_day) + ".csv")))


def potential_uptrend_from_lows():
    # small market cap stocks with few shares outstanding
    filters = ['sh_avgvol_o400','ta_pattern_channelup','ta_perf_1wdown']
    stock_list = Screener(filters=filters, table='Performance', order='price')

    # Export the screener results to .csv
    stock_list.to_csv(os.path.join(folder_path, ("potential uptrend from lows\\" + str(last_business_day) + ".csv")))


def short_squeeze():
    # small market cap stocks with few shares outstanding
    filters = ['sh_avgvol_o100','sh_instown_u50','sh_price_o2','sh_short_o15']
    stock_list = Screener(filters=filters, table='Performance')

    # Export the screener results to .csv
    stock_list.to_csv(os.path.join(folder_path, ("short squeeze\\" + str(last_business_day) + ".csv")))


def shorted_stocks():
    # small market cap stocks with few shares outstanding
    filters = ['cap_smallover','geo_usa','sh_avgvol_o500','sh_curvol_o500','sh_opt_optionshort','sh_price_o3','sh_relvol_o1','sh_short_high']
    stock_list = Screener(filters=filters, table='Performance', order='price')

    # Export the screener results to .csv
    stock_list.to_csv(os.path.join(folder_path, ("shorted stocks\\" + str(last_business_day) + ".csv")))

def sma_crossover():
    # small market cap stocks with few shares outstanding
    filters = ['fa_pe_profitable','sh_avgvol_o400','sh_relvol_o1','sh_short_low','ta_beta_o1','ta_sma50_cross20b']
    stock_list = Screener(filters=filters, table='Performance', order='price')

    # Export the screener results to .csv
    stock_list.to_csv(os.path.join(folder_path, ("sma crossover\\" + str(last_business_day) + ".csv")))


def undervalued_dividend_growth():
    # small market cap stocks with few shares outstanding
    filters = ['cap_largeover','fa_div_pos','fa_epsyoy1_o5','fa_estltgrowth_o5','fa_payoutratio_u50','fa_pe_u20','fa_peg_low']
    stock_list = Screener(filters=filters, table='Performance', order='price')

    # Export the screener results to .csv
    stock_list.to_csv(os.path.join(folder_path, ("undervalued dividend growth\\" + str(last_business_day) + ".csv")))

def top_gainers():
    # small market cap stocks with few shares outstanding
    filters = ['ta_topgainers']
    stock_list = Screener(filters=filters, table='Performance', order='Change')

    path = os.path.join(folder_path, ("top gainers\\" + str(last_business_day) + ".csv"))

    my_df = pd.DataFrame(stock_list[-20:])

    my_df.to_csv(path, index=False, mode='w', header=['No.','Ticker', 'Perf Week', 'Perf Month', 'Perf Quart', 'Perf Half',
                              'Perf Year', 'Perf YTD', 'Volatility W', 'Volatility M',
                              'Recom', 'Avg Volume', 'Rel Volume', 'Price', 'Change',
                              'Volume'])


def top_losers():
    # small market cap stocks with few shares outstanding
    filters = ['ta_toplosers']
    stock_list = Screener(filters=filters, table='Performance', order='Change')

    path = os.path.join(folder_path, ("top losers\\" + str(last_business_day) + ".csv"))

    my_df = pd.DataFrame(stock_list[0:20])


    my_df.to_csv(path, index=False, mode='w', header=['No.','Ticker', 'Perf Week', 'Perf Month', 'Perf Quart', 'Perf Half',
                              'Perf Year', 'Perf YTD', 'Volatility W', 'Volatility M',
                              'Recom', 'Avg Volume', 'Rel Volume', 'Price', 'Change',
                              'Volume'])


def low_rsi():
    # small market cap stocks with few shares outstanding
    filters = ['ta_rsi_os30']
    stock_list = Screener(filters=filters, order = 'RSI')

    path = os.path.join(folder_path, ("low rsi\\" + str(last_business_day) + ".csv"))

    my_df = pd.DataFrame(stock_list[0:450])

    my_df.to_csv(path, index=False)


def forte_capital():
    # small market cap stocks with few shares outstanding
    filters = ['ipodate_prev3yrs','sh_avgvol_o500','sh_short_o5','ta_changeopen_u','ta_sma20_pa','ta_sma200_pa', 'ta_sma50_pa']
    stock_list = Screener(filters=filters)

    path = os.path.join(folder_path, ("forte capital\\" + str(last_business_day) + ".csv"))

    my_df = pd.DataFrame(stock_list[0:300])

    my_df.to_csv(path, index=False)


def undervalued():
    # small market cap stocks with few shares outstanding
    filters = ['fa_curratio_o2','fa_div_o3','fa_fpe_low','fa_pc_o5','fa_pe_low','fa_pfcf_o']
    stock_list = Screener(filters=filters)

    path = os.path.join(folder_path, ("undervalued\\" + str(last_business_day) + ".csv"))

    my_df = pd.DataFrame(stock_list[0:300])

    my_df.to_csv(path, index=False)


def earnings_high_eps():
    # small market cap stocks with few shares outstanding
    filters = ['earningsdate_nextdays5','fa_curratio_o2','fa_eps5years_o5','fa_epsqoq_o5','fa_epsyoy_o5','fa_epsyoy1_o5','fa_estltgrowth_o5', 'fa_quickratio_o2','fa_sales5years_o5']
    stock_list = Screener(filters=filters)

    path = os.path.join(folder_path, ("earnings high EPS\\" + str(last_business_day) + ".csv"))

    my_df = pd.DataFrame(stock_list[0:300])

    my_df.to_csv(path, index=False)


def top_gainers_averages():
    # small market cap stocks with few shares outstanding
    filters = ['fa_epsyoy_neg', 'sh_price_u50', 'ta_perf_52w300o']
    stock_list = Screener(filters=filters)

    path = os.path.join(folder_path, ("top gainers averages\\" + str(last_business_day) + ".csv"))

    stock_list.to_csv(path)


def undervalued_two():
    # small market cap stocks with few shares outstanding
    filters = ['fa_div_pos','fa_pb_low','fa_pe_low','fa_peg_low']
    stock_list = Screener(filters=filters)

    path = os.path.join(folder_path, ("undervalued two\\" + str(last_business_day) + ".csv"))

    my_df = pd.DataFrame(stock_list[0:300])

    my_df.to_csv(path, index=False)


def support_level():
    # small market cap stocks with few shares outstanding
    filters = ['ta_p_tlsupport', 'sh_avgvol_o400','ta_pattern_channelup','ta_perf_1wdown']
    stock_list = Screener(filters=filters)

    path = os.path.join(folder_path, ("support level\\" + str(last_business_day) + ".csv"))

    my_df = pd.DataFrame(stock_list[0:300])

    my_df.to_csv(path, index=False)


def all_stocks():
    # small market cap stocks with few shares outstanding
    filters = ['s=ta_topgainers']
    stock_list = Screener(filters=filters, table='Performance', order='Change')

    # Export the screener results to .csv
    stock_list.to_csv(os.path.join(folder_path, ("all stocks\\" + str(last_business_day) + ".csv")))


def five_times_rel_vol():
    # small market cap stocks with few shares outstanding
    filters = ['sh_relvol_o5']
    stock_list = Screener(filters=filters, table='Performance', order='price')

    # Export the screener results to .csv
    stock_list.to_csv(os.path.join(folder_path, ("5x rel vol\\" + str(last_business_day) + ".csv")))


def rel_vol_pattern():
    # small market cap stocks with few shares outstanding
    filters = ['cap_smallunder', 'fa_pb_high', 'fa_ps_o5', 'ta_averagetruerange_o2']
    stock_list = Screener(filters=filters)

    my_df = pd.DataFrame(stock_list[0:200])

    my_df.to_csv(os.path.join(folder_path, ("rel vol pattern\\" + str(last_business_day) + ".csv")), index=False)


try:
    low_rsi()
    time.sleep(15)
except Exception as e:
    print("low rsi: " + str(e))

try:
    top_gainers_averages()
    time.sleep(15)
except Exception as e:
    print("top gainers averages: " + str(e))

try:
    top_losers()
    time.sleep(15)
except Exception as e:
    print("top losers: " + str(e))

try:
    top_gainers()
    time.sleep(15)
except Exception as e:
    print("rel vol pattern: " + str(e))

try:
    rel_vol_pattern()
    time.sleep(15)
except Exception as e:
    print("rel vol pattern: " + str(e))

try:
    five_times_rel_vol()
    time.sleep(15)
except Exception as e:
    print("five times rel vol: " + str(e))

try:
    all_stocks()
    time.sleep(15)
except Exception as e:
    print("all stocks: " + str(e))

try:
    undervalued_two()
    time.sleep(15)
except Exception as e:
    print("undervalued two: " + str(e))

try:
    earnings_high_eps()
    time.sleep(15)
except Exception as e:
    print("earnings high eps: " + str(e))

try:
    undervalued()
    time.sleep(15)
except Exception as e:
    print("undervalued: " + str(e))

try:
    forte_capital()
    time.sleep(15)
except Exception as e:
    print("forte capital: " + str(e))


try:
    analysts_buy()
    time.sleep(15)
except Exception as e:
    print("analysts buy: " + str(e))


try:
    small_mc_rel_vol()
    time.sleep(15)
except Exception as e:
    print("small mc rel vol: " + str(e))

try:
    bankruptcy_squeeze_candidates()
    time.sleep(15)
except Exception as e:
    print("bankruptcy squeeze candidates" + str(e))

try:
    bounce_at_moving_average()
    time.sleep(15)
except Exception as e:
    print("bounce at moving average: " + str(e))

try:
    breaking_out()
    time.sleep(15)
except Exception as e:
    print("breaking out: " + str(e))

try:
    buy_and_hold_value()
    time.sleep(15)
except Exception as e:
    print("buy and hold value: " + str(e))

try:
    canslim()
    time.sleep(15)
except Exception as e:
    print("canslim: " + str(e))

try:
    consistent_growth_bullish_trend()
    time.sleep(15)
except Exception as e:
    print("consistent growth bullish trend: " + str(e))

try:
    earnings_gap_up()
    time.sleep(15)
except Exception as e:
    print("earnings gap up: " + str(e))

try:
    high_earnings_growth()
    time.sleep(15)
except Exception as e:
    print("high earnings growth: " + str(e))

try:
    high_relative_volume()
    time.sleep(15)
except Exception as e:
    print("high relative volume: " + str(e))

try:
    low_pe_value()
    time.sleep(15)
except Exception as e:
    print("low pe value: " + str(e))

try:
    new_highs()
    time.sleep(15)
except Exception as e:
    print("new highs: " + str(e))

try:
    oversold_reversal()
    time.sleep(15)
except Exception as e:
    print("oversold reversal: " + str(e))

try:
    oversold_upcoming_earnings()
    time.sleep(15)
except Exception as e:
    print("oversold upcoming earnings: " + str(e))

try:
    potential_uptrend_from_lows()
    time.sleep(15)
except Exception as e:
    print("potential uptrend from lows: " + str(e))

try:
    short_squeeze()
    time.sleep(15)
except Exception as e:
    print("short squeeze: " + str(e))

try:
    shorted_stocks()
    time.sleep(15)
except Exception as e:
    print("shorted stocks: " + str(e))

try:
    sma_crossover()
    time.sleep(15)
except Exception as e:
    print("sma crossover: " + str(e))

try:
    undervalued_dividend_growth()
    time.sleep(15)
except Exception as e:
    print("undervalued dividend growth: " + str(e))

