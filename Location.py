import requests
import bs4
from datetime import datetime 
##Get the current location of the device from it's IP##
#object has attributes [.city, .state, .country, .country_code, .lat, .long ] once get_location is called.
class InvalidScrapeException(Exception):
    "Raised when the scraping is unseccessful in finding correct tag"
    pass
        
class IPLocation():

    def __init__(self):
        self.city  = ''
        self.state = ''
        self.country = ''
        self.country_code = ''
        self.lat = 0
        self.long = 0
        self.sunrise = datetime.now()
        self.sunset = datetime.now()

    def get_location(self): #

        try:

            #checks if the current element at [2] is the IP Location and if so, saves the city and state and country code
            scrape_result = requests.get("https://www.iplocation.net/")
            scraped_soup = bs4.BeautifulSoup(scrape_result.text,"lxml")
            span_element = scraped_soup.find('span', class_='ipinfo--location')

            self.element  = span_element.text.split('  ')[0]
            print(self.element)

            # self.element = scraped_soup.select('th')[2].getText()
            if not self.element:
                raise InvalidScrapeException
                
            # self.location = scraped_soup.select('td')[2].getText()
            self.element = self.element.replace(",","")
            #parse location into city/state/country
            self.city = self.element.split()[0]
            self.state = self.element.split()[1]
            self.country = self.element.split()[2][1:3]


            #return list((self.city,self.state,self.country, [two datetime placeholders]))

           
            
        except InvalidScrapeException:
            print(f" Received '{self.element}' instead of 'IP Location'.")
            
            

    def __str__ (self):
        return f"The user is in {self.city}, {self.state}, in country code {self.country}."\

