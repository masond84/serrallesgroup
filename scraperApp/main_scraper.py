#### Web Scraper Algorithm ####
'''
The client essentially wants a web-scraper that will gather relevant information from this site.
https://hillsborough.realforeclose.com/

The scraper should be able to go through EACH county within Florida. Next the program should sort through
auctions every single day, the site allows a convenient look into auctions sorted by date.
Go To:
'Auction Calendar' -> Select The Appropriate Calendar Date (Most Recent/Daily) ->  View All Auctions
There are Auction Categories: 1. Running Auctions 2. Auctions Waiting 3. Auctions Closed or Canceled
'''
# import modules
#import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import date
from django.conf import settings
import os
import time
from time import sleep 
import pandas as pd
from .emailer import send_email
from .scraper_functions import visit_auction_pages, clean_excel_file

def store_all_data(driver, urls_to_visit, target_date):
    # Initialize an empty DataFrame with the same columns as your data
    all_data = pd.DataFrame(columns=['Auction Sold', 'Amount', 'Sold To', 'Auction Type:', 'Case #:',
        'Final Judgment Amount:', 'Parcel ID:', 'Property Address:', '',
        'Assessed Value:', 'Plaintiff Max Bid:', 'Auction Status'])
    # Iterate through the list of URLs and scrape data
    for url in urls_to_visit:
        df = visit_auction_pages(driver, url, target_date)
        all_data = pd.concat([all_data, df], ignore_index=True)

    return all_data

def run_scraper():        
    # Define a list of URLs to visit
    all_urls = ['https://myorangeclerk.realforeclose.com/index.cfm?resetcfcobjs=1']#, 'https://volusia.realforeclose.com/index.cfm?resetcfcobjs=1',
                #'https://hillsborough.realforeclose.com/index.cfm', 'https://alachua.realforeclose.com/index.cfm?resetcfcobjs=1',
                #'https://alachua.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://baker.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://bay.realforeclose.com/index.cfm?resetcfcobjs=1', 
                #'https://bay.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://brevard.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://broward.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://calhoun.realforeclose.com/index.cfm?resetcfcobjs=1',
                #'https://charlotte.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://citrus.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://citrus.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://clay.realforeclose.com/index.cfm?resetcfcobjs=1', 
                #'https://clay.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://duval.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://duval.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://escambia.realforeclose.com/index.cfm?resetcfcobjs=1', 
                #'https://escambia.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://flagler.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://flagler.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://gilchrist.realforeclose.com/index.cfm?resetcfcobjs=1', 
                #'https://gilchrist.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://gulf.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://gulf.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://hendry.realtaxdeed.com/index.cfm?resetcfcobjs=1', 
                #'https://hernando.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://hillsborough.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://indian-river.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://indian-river.realtaxdeed.com/index.cfm?resetcfcobjs=1', 
                #'https://jackson.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://jackson.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://lake.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://lee.realforeclose.com/index.cfm?resetcfcobjs=1', 
                #'https://lee.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://leon.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://leon.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://manatee.realforeclose.com/index.cfm?resetcfcobjs=1', 
                #'https://marion.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://marion.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://martin.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://martin.realtaxdeed.com/index.cfm?resetcfcobjs=1', 
                #'https://miamidade.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://nassauclerk.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://nassau.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://okaloosa.realforeclose.com/index.cfm?resetcfcobjs=1', 
                #'https://okaloosa.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://okeechobee.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://orange.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://osceola.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://palmbeach.realforeclose.com/index.cfm?resetcfcobjs=1', 
                #'https://palmbeach.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://pasco.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://pasco.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://pinellas.realforeclose.com/index.cfm?resetcfcobjs=1', 
                #'https://pinellas.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://polk.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://polk.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://putnam.realforeclose.com/index.cfm?resetcfcobjs=1', 
                #'https://putnam.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://saintjohns.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://santarosa.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://santarosa.realtaxdeed.com/index.cfm?resetcfcobjs=1', 
                #'https://sarasota.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://sarasota.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://seminole.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://stlucie.realforeclose.com/index.cfm?resetcfcobjs=1', 
                #'https://volusia.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://walton.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://washington.realforeclose.com/index.cfm?resetcfcobjs=1', 
                #'https://washington.realtaxdeed.com/index.cfm?resetcfcobjs=1']

    # Create a Chrome WebDriver instance
    options = Options()
    driver = webdriver.Chrome(options=options)

    # Specify the target date
    #target_date = datetime.now()
    target_date = date(2023, 10, 6)

    raw_data = store_all_data(driver, all_urls, target_date)
    print(raw_data)

    # Close the WebDriver
    driver.quit()

    # Specify the base path and extension for the Excel file
    base_path = os.path.join(settings.MEDIA_ROOT, 'excel_files')
    extension = "xlsx"

    # Get the current date and time, and format as string
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create a unique filename by appending the date and time
    unique_filename = f"raw_data_{current_datetime}"
    # Combine the base path and extension to create the full file path
    file_path = f"{base_path}\{unique_filename}.{extension}"
    # Save the combined DataFrame to the specified file path
    raw_data.to_excel(file_path, index=False)

    # Create a unique filename by appending the date and time
    cleaned_filename = f"cleaned_{current_datetime}"
    # Combine the base path and extension to create the full file path
    cleaned_file_path = f"{base_path}\{cleaned_filename}.{extension}"
    # Clean the raw excel file
    output_path = clean_excel_file(file_path, cleaned_file_path)

    print(f"Data saved to {file_path}")

    ## Send email of the data ##
    subject = "Daily Auction Report"
    message = "Here is the auction data for all counties in florida for today."
    attachment_paths = [file_path, cleaned_file_path]
    send_email(subject, message, attachment_paths)
###############
## MAIN CODE ##
###############
# Define a list of URLs to visit
all_urls = ['https://myorangeclerk.realforeclose.com/index.cfm?resetcfcobjs=1']#, 'https://volusia.realforeclose.com/index.cfm?resetcfcobjs=1',
            #'https://hillsborough.realforeclose.com/index.cfm', 'https://alachua.realforeclose.com/index.cfm?resetcfcobjs=1',
            #'https://alachua.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://baker.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://bay.realforeclose.com/index.cfm?resetcfcobjs=1', 
            #'https://bay.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://brevard.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://broward.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://calhoun.realforeclose.com/index.cfm?resetcfcobjs=1',
            #'https://charlotte.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://citrus.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://citrus.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://clay.realforeclose.com/index.cfm?resetcfcobjs=1', 
            #'https://clay.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://duval.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://duval.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://escambia.realforeclose.com/index.cfm?resetcfcobjs=1', 
            #'https://escambia.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://flagler.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://flagler.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://gilchrist.realforeclose.com/index.cfm?resetcfcobjs=1', 
            #'https://gilchrist.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://gulf.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://gulf.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://hendry.realtaxdeed.com/index.cfm?resetcfcobjs=1', 
            #'https://hernando.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://hillsborough.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://indian-river.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://indian-river.realtaxdeed.com/index.cfm?resetcfcobjs=1', 
            #'https://jackson.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://jackson.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://lake.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://lee.realforeclose.com/index.cfm?resetcfcobjs=1', 
            #'https://lee.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://leon.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://leon.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://manatee.realforeclose.com/index.cfm?resetcfcobjs=1', 
            #'https://marion.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://marion.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://martin.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://martin.realtaxdeed.com/index.cfm?resetcfcobjs=1', 
            #https://miamidade.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://nassauclerk.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://nassau.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://okaloosa.realforeclose.com/index.cfm?resetcfcobjs=1', 
            #'https://okaloosa.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://okeechobee.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://orange.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://osceola.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://palmbeach.realforeclose.com/index.cfm?resetcfcobjs=1', 
            #'https://palmbeach.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://pasco.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://pasco.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://pinellas.realforeclose.com/index.cfm?resetcfcobjs=1', 
            #'https://pinellas.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://polk.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://polk.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://putnam.realforeclose.com/index.cfm?resetcfcobjs=1', 
            #'https://putnam.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://saintjohns.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://santarosa.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://santarosa.realtaxdeed.com/index.cfm?resetcfcobjs=1', 
            #'https://sarasota.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://sarasota.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://seminole.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://stlucie.realforeclose.com/index.cfm?resetcfcobjs=1', 
            #'https://volusia.realtaxdeed.com/index.cfm?resetcfcobjs=1', 'https://walton.realforeclose.com/index.cfm?resetcfcobjs=1', 'https://washington.realforeclose.com/index.cfm?resetcfcobjs=1', 
            #'https://washington.realtaxdeed.com/index.cfm?resetcfcobjs=1']
