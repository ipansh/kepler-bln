from selenium import webdriver
import json
import scrapy
import scraper
from scrapy import Selector
import requests
import pandas as pd
import time
import telegram_notifier
from sqlalchemy import create_engine, text
import os

telegram_token = os.environ.get("TELEGRAM_TOKEN")
db_access_key = os.environ.get("POSTGRE")

if __name__  == '__main__': 
    cnx = create_engine(db_access_key)
    sql = '''select * from public.wg_listings;'''
    query = text(sql)
    current_df = pd.read_sql_query(query, cnx)
    print('Obtained master table!')
    listings_list = scraper.get_wg_gesucht_listings()
    final_df = scraper.scrape_wg_gesucht_data(listings_list)
    filtered_df = scraper.clean_and_filter_gesucht_data(final_df)
    new_df = current_df.append(filtered_df)
    new_df = new_df.reset_index().drop(columns = ['index'])
    new_df['id'] = [i for i in range(1,len(new_df)+1)]
    new_df['notified'] = new_df['notified'].fillna('no')
    new_df = new_df.drop_duplicates(subset = ['url'])
    for url, notified in zip(new_df['url'],new_df['notified']):
        if notified == 'no':
            telegram_notifier.send_message('https://www.wg-gesucht.de'+url, telegram_token)
        else:
            pass
    print('Message should be sent.')
    new_df['notified'] = 'yes'
    new_df.to_sql('wg_listings', cnx, schema = 'public', index = False, chunksize=100, if_exists='replace', method = 'multi')
    print('All tasks completed!')