import sys
import os
from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from .scraper_functions import visit_auction_pages  # Import your scraping function
from datetime import datetime

def index_view(request):
    return render(request, 'scraperApp/index.html')

url_to_county = {
    'orange': 'https://myorangeclerk.realforeclose.com/index.cfm?resetcfcobjs=1',
    'volusia': 'https://volusia.realforeclose.com/index.cfm?resetcfcobjs=1',
    'hillsborough': 'https://hillsborough.realforeclose.com/index.cfm',
    'alachua': 'https://alachua.realforeclose.com/index.cfm?resetcfcobjs=1',
    'alachua2': 'https://alachua.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'baker': 'https://baker.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'bay': 'https://bay.realforeclose.com/index.cfm?resetcfcobjs=1',
    'bay2': 'https://bay.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'brevard': 'https://brevard.realforeclose.com/index.cfm?resetcfcobjs=1',
    'broward': 'https://broward.realforeclose.com/index.cfm?resetcfcobjs=1',
    'calhoun': 'https://calhoun.realforeclose.com/index.cfm?resetcfcobjs=1',
    'charlotte': 'https://charlotte.realforeclose.com/index.cfm?resetcfcobjs=1',
    'citrus': 'https://citrus.realforeclose.com/index.cfm?resetcfcobjs=1',
    'citrus2': 'https://citrus.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'clay': 'https://clay.realforeclose.com/index.cfm?resetcfcobjs=1',
    'clay2': 'https://clay.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'duval': 'https://duval.realforeclose.com/index.cfm?resetcfcobjs=1',
    'duval2': 'https://duval.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'escambia': 'https://escambia.realforeclose.com/index.cfm?resetcfcobjs=1',
    'escambia2': 'https://escambia.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'flagler': 'https://flagler.realforeclose.com/index.cfm?resetcfcobjs=1',
    'flagler2': 'https://flagler.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'gilchrist': 'https://gilchrist.realforeclose.com/index.cfm?resetcfcobjs=1',
    'gilchrist2': 'https://gilchrist.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'gulf': 'https://gulf.realforeclose.com/index.cfm?resetcfcobjs=1',
    'gulf2': 'https://gulf.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'hendry': 'https://hendry.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'hernando': 'https://hernando.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'hillsborough2': 'https://hillsborough.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'indianriver': 'https://indian-river.realforeclose.com/index.cfm?resetcfcobjs=1',
    'indianriver2': 'https://indian-river.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'jackson': 'https://jackson.realforeclose.com/index.cfm?resetcfcobjs=1',
    'jackson2': 'https://jackson.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'lake': 'https://lake.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'lee': 'https://lee.realforeclose.com/index.cfm?resetcfcobjs=1',
    'lee2': 'https://lee.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'leon': 'https://leon.realforeclose.com/index.cfm?resetcfcobjs=1',
    'leon2': 'https://leon.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'manatee': 'https://manatee.realforeclose.com/index.cfm?resetcfcobjs=1',
    'marion': 'https://marion.realforeclose.com/index.cfm?resetcfcobjs=1',
    'marion2': 'https://marion.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'martin': 'https://martin.realforeclose.com/index.cfm?resetcfcobjs=1',
    'martin2': 'https://martin.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'miamidade': 'https://miamidade.realforeclose.com/index.cfm?resetcfcobjs=1',
    'nassau': 'https://nassauclerk.realforeclose.com/index.cfm?resetcfcobjs=1',
    'nassau2': 'https://nassau.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'okaloosa': 'https://okaloosa.realforeclose.com/index.cfm?resetcfcobjs=1',
    'okaloosa2': 'https://okaloosa.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'okeechobee': 'https://okeechobee.realforeclose.com/index.cfm?resetcfcobjs=1',
    'orange2': 'https://orange.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'osceola': 'https://osceola.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'palmbeach': 'https://palmbeach.realforeclose.com/index.cfm?resetcfcobjs=1',
    'palmbeach2': 'https://palmbeach.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'pasco': 'https://pasco.realforeclose.com/index.cfm?resetcfcobjs=1',
    'pasco2': 'https://pasco.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'pinellas': 'https://pinellas.realforeclose.com/index.cfm?resetcfcobjs=1',
    'pinellas2': 'https://pinellas.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'polk': 'https://polk.realforeclose.com/index.cfm?resetcfcobjs=1',
    'polk2': 'https://polk.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'putnam': 'https://putnam.realforeclose.com/index.cfm?resetcfcobjs=1',
    'putnam2': 'https://putnam.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'saintjohns': 'https://saintjohns.realforeclose.com/index.cfm?resetcfcobjs=1',
    'santarosa': 'https://santarosa.realforeclose.com/index.cfm?resetcfcobjs=1',
    'santarosa2': 'https://santarosa.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'sarasota': 'https://sarasota.realforeclose.com/index.cfm?resetcfcobjs=1',
    'sarasota2': 'https://sarasota.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'seminole': 'https://seminole.realforeclose.com/index.cfm?resetcfcobjs=1',
    'stlucie': 'https://stlucie.realforeclose.com/index.cfm?resetcfcobjs=1',
    'volusia2': 'https://volusia.realtaxdeed.com/index.cfm?resetcfcobjs=1',
    'walton': 'https://walton.realforeclose.com/index.cfm?resetcfcobjs=1',
    'washington': 'https://washington.realforeclose.com/index.cfm?resetcfcobjs=1',
    'washington2': 'https://washington.realtaxdeed.com/index.cfm?resetcfcobjs=1',
}

# Create your views here.
def scrape_view(request):
    if request.method == 'POST':
        county = request.POST['county']
        auction_date_str = request.POST['auction_date']
        try:
            # Convert the date string to a datetime object
            target_date = datetime.strptime(auction_date_str, '%Y-%m-%d')
        except ValueError:
            # Handle invalid date format here
            return HttpResponse('Invalid date format', status=400)
        
        url = url_to_county.get(county)

        if url:
            # Intitialize a WebDriver
            options = Options()
            driver = webdriver.Chrome(options=options)

            data_frame = visit_auction_pages(driver, url, target_date)

            driver.quit()

            # Create a CSV response
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="scraped_data.csv"'

            # Write the data_frame to the response in CSV format
            data_frame.to_csv(response, index=False, encoding='utf-8')

            return response
        
    return render(request, 'scraperApp/index.html')