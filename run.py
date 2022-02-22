from scraper import Verge_scraper


# Checking linting
#Let's see if the linting is working or not
try:
    with Verge_scraper(keyword="", year="2021", month="Feb") as bot:
        bot.land_req_page()
        bot.load_more()
        bot.info_extractor()
        bot.write_to_csv()
        bot.print_table()
except Exception as e:
    print(e)
