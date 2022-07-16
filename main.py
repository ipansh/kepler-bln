import os
import scraper

if __name__  == '__main__': 
    listings_list = scraper.get_wg_gesucht_listings()
    final_df = scraper.scrape_wg_gesucht_data(listings_list)
    filtered_df = scraper.clean_and_filter_gesucht_data(final_df)
    print('Done!')