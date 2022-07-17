import os
import scraper
import telegram_notifier
import gspread_wrapper

telegram_token = os.environ.get("TELEGRAM_TOKEN")

if __name__  == '__main__': 
    master_df = gspread_wrapper.get_master_spreadsheet()
    print('Obtained master spreadsheet!')
    listings_list = scraper.get_wg_gesucht_listings()
    final_df = scraper.scrape_wg_gesucht_data(listings_list)
    filtered_df = scraper.clean_and_filter_gesucht_data(final_df)
    telegram_notifier.send_message('Job done!',telegram_token)
    print('Done!')