import datetime
weekno = datetime.datetime.today().weekday()

if 6 > weekno > 0:
    import FinVizScraper
    import TickerExtractor
    import LongTermRecords
    import RSIcrossover