import requests
import bs4

##Get the current location of the device from it's IP##

class InvalidScrapeException(Exception):
    "Raised when the scraping is unseccessful in finding correct tag"
    pass
        
class Location_From_IP():

    def __init__(self):
        self.city  = ''
        self.state = ''
        self.country = ''
        self.time = 0

    def get_location(self):

        try:

            #checks if the current element at [2] is the IP Location and if so, saves the city and state and country code
            scrape_result = requests.get("https://www.iplocation.net/")
            scraped_soup = bs4.BeautifulSoup(scrape_result.text,"lxml")
            self.element = scraped_soup.select('th')[2].getText()
            
            if self.element == "IP Location":
                
                self.location = scraped_soup.select('td')[2].getText()
                self.location = self.location.replace(",","")

                #parse location into city/state/country
                self.city = self.location.split()[0]
                self.state = self.location.split()[1]
                self.country = self.location.split()[2][1:3]

            else:
                raise InvalidScrapeException
            
        except InvalidScrapeException:
            print(f" Received '{self.element}' instead of 'IP Location'.")
            

    def __str__ (self):
        return f"The user is in {self.city}, {self.state}, in country code {self.country}."

    
TL = Location_From_IP()

TL.get_location()
print(TL)

