from scrapy import Selector
import requests
import pandas as pd
import time
from selenium import webdriver

def get_wg_gesucht_listings():
    url = 'https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.1.0.html#back_to_ad_9161625'
    html = requests.get(url).text
    sel = Selector(text = html)
    listings_list = list(sel.xpath('//*[contains(@class,"wgg_card offer_list_item  ")]/div/div/a/@href').extract())
    listings_list = list(set(listings_list))
    return [listing for listing in listings_list if listing.endswith('html')]

def scrape_wg_gesucht_data(input_list):
    """Function for scraping data from each individual listing."""
    appended_data = []
    counter = 0
    for listing in input_list:
        try:
            print(listing)
            #try:
            listing_html = 'https://www.wg-gesucht.de/'+listing
            html = requests.get(listing_html).text
            sel = Selector(text = html)
            apartment_dict = {}
            print('listing...', end = ' ')
            apartment_dict['url'] = listing_html
            #1. listing size
            print('size...', end = ' ')
            apartment_dict['size'] = sel.xpath('//*[contains(@class,"headline headline-key-facts")]/text()').extract()[0].strip() 
            #2. rent
            print('rent...', end = ' ')
            apartment_dict['rent'] = sel.xpath('//*[contains(@class,"headline headline-key-facts")]/text()').extract()[2].strip()   
            #3. rooms
            print('rooms...', end = ' ')
            if len(sel.xpath('//*[contains(@class,"headline headline-key-facts")]/text()').extract()) == 6:
                apartment_dict['rooms'] = sel.xpath('//*[contains(@class,"headline headline-key-facts")]/text()').extract()[4].strip()
            else:
                pass
            #4. floor
            #print('floor...', end = ' ')
            #raw_floor = sel.xpath('//*[contains(@class,"col-xs-6 col-sm-4 text-center print_text_left")]/text()').extract()[2]
            #apartment_dict['floor'] = ''.join(raw_floo r.split())
            #5. deposit
            print('deposit...', end = ' ')
            if sel.xpath('//*[contains(@id,"kaution")]/@value') != []:
                apartment_dict['deposit'] = sel.xpath('//*[contains(@id,"kaution")]/@value').extract()[0]
            else:
                pass
            #6. address_street
            print('street...', end = ' ')
            raw_street = sel.xpath('//*[contains(@class,"col-sm-4 mb10")]/a/text()').extract()[0]
            apartment_dict['street'] = ' '.join(raw_street.split())
            #7. district
            print('location...', end = ' ')
            raw_district = sel.xpath('//*[contains(@class,"col-sm-4 mb10")]/a/text()').extract()[1]
            apartment_dict['location'] = ' '.join(raw_district.split())
            #8. available_from
            print('available from...', end = ' ')
            apartment_dict['available_from'] = sel.xpath('//*[contains(@class,"col-sm-3")]/p/b/text()').extract()[0]
            #9. term
            #available_until
            print('available until...')
            if 'frei bis:' in [item.strip() for item in sel.xpath('//*[contains(@class,"col-sm-3")]/p/text()').extract()]:
                output_term = sel.xpath('//*[contains(@class,"col-sm-3")]/p/b/text()').extract()[1]
            else:
                output_term = 'unlimited'
            apartment_dict['available_until'] = output_term
            #10. tausch
            if 'Tauschangebot' in [item.strip() for item in sel.xpath('//*[contains(@class,"col-sm-3")]/p/text()').extract()]:
                tausch = True
            else:
                tausch = False
            apartment_dict['tausch'] = tausch
            appended_data.append(apartment_dict)
            counter = counter+1
            if counter%10 == 0:
                print('Aggregated listings: {}.'.format(counter), end = ' ')
                time.sleep(10)
        except:
            listing+' passed!'
            pass
    df = pd.DataFrame(appended_data)
    df = df.reset_index().rename(columns = {'index':'id'})
    return df

def clean_and_filter_gesucht_data(final_df):
    final_df['size'] = [int(size.strip('m²')) for size in final_df['size']]
    final_df['rent'] = [int(rent.strip('€')) for rent in final_df['rent']]
    final_df['district'] = [location.split(' ')[-1] for location in final_df['location']]
    final_df['zipcode'] = [location.split(' ')[0] for location in final_df['location']]
    filtered_df = final_df[(final_df['rent'] < 1500) &
                       (final_df['available_until'] == 'unlimited') &
                       (final_df['tausch'] == False)]
                       #(final_df['district'].isin(['Pankow','Charlottenburg','Mitte','Berg','Wedding']))]
    filtered_df = filtered_df[['url','size','rent','rooms','deposit','street','district','zipcode','available_from']]
    return filtered_df


def scrape_ebay(selenium_driver):
    selenium_driver.get("https://www.ebay-kleinanzeigen.de/s-wohnung-mieten/berlin/c203l3331")
    selenium_response = selenium_driver.page_source

    new_selector = Selector(text=selenium_response)

    listings = new_selector.xpath('//*[contains(@class,"text-module-begin")]/a/@href').extract()

    print(listings)

    #items = new_selector.xpath('//*[@class="house-item clearfix"]/a/@href').extract()

    #items = list(set(['https://www.wellcee.com'+listing_id for listing_id in items]))

    return print(selenium_response)