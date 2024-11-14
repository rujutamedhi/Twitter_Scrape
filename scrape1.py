#used selenium for navigation and beautiful soup to target element and scrape them
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import traceback
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
chrome_options = Options()

# Initialize Selenium WebDriver with ChromeDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the CSV file and set up lists to store the scraped data
with open('C:\\projects\\ATG_2nd_Round\\twitter_links.csv', mode='r', newline='', encoding='utf-8') as file:

    #to read csv file
    csv_reader = csv.reader(file)

    #lists to store details
    bio = []
    followings = []
    followers = []
    location = []
    website = []

    #flag to only implement time sleep of 100 sec for first iteration..This is done so that I get time to login to my Twitter account.
    first_itr =True

    # Iterate over each row in the CSV file
    for row in csv_reader:
        url = row[0]
        print(f"Scraping URL: {url}")

        try:
            # Using Selenium to open the URL
            driver.get(url)
            if(first_itr):
            # Wait for the page to load 
               time.sleep(100)
               first_itr=False
            time.sleep(15)
            WebDriverWait(driver, 50).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'body'))
            )
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            #box contains all information
            box = soup.find("div", class_="css-175oi2r r-3pj75a r-ttdzmv r-1ifxtd0")
            
            #Since all have same class name, I have scraped all the span having the class mentioned below
            findall=box.find_all("span",class_="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3")

            # only consider elements which will have following class names.No other class names.
            target_classes = ["css-1jxf684", "r-bcqeeo", "r-1ttztb7", "r-qvutc0", "r-poiln3"]

            #elements having other class names are not added to the list below
            filtered_items = []

            # I am removing items that have "Translate bio" or "." or class name other than mentioned above
            for item in findall:
                classes = item.get('class', [])
                # Only process items that match the target classes and do not contain "Translate bio"
                if sorted(classes) == sorted(target_classes) and ("Translate bio" not in item.text or "." not in item.text):
                 filtered_items.append(item)

            #The list contains bio at index 3
            bio_info=filtered_items[len(filtered_items)-10]

            #Appending bio_info scraped to the bio list defined earlier.
            bio.append(bio_info.text.strip() if bio_info else "Not available")

            #Calculated the index of following count and then appended it to list
            following = findall[len(findall)-5]  
            followings.append(following.text.strip() if following else "Not available")

            #Calculated the index of followers count and then appended it to list
            follower = findall[len(findall)-3]  
            followers.append(follower.text.strip() if follower else "Not available")

            #Calculated the index of location and then appended it to list
            loc=findall[len(findall)-9]
            location.append(loc.text.strip() if loc else "Not available")

            #Calculated the index of website link and then appended it to list
            link=box.find('a',class_="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3 r-4qtqp9 r-1a11zyx r-1loqt21")
            website.append(link.get('href').strip() if link else "Not available")

        
        #If there was any error during execution,this will run
        except Exception as e:
            print("An error occurred:", e)
            print(traceback.format_exc())
            bio.append('Not available')
            followings.append('Not available')
            followers.append('Not available')
            location.append('Not available')
            website.append('Not available')

# Close the Selenium WebDriver when done
driver.quit()

# Adding data to csv file
with open('Twitter.csv', mode='w', newline='', encoding='utf-8') as output_file:
    csv_writer = csv.writer(output_file)
    # Write headers
    csv_writer.writerow(["Bio", "Following", "Followers", "Location", "Website"])
    # Write data
    for i in range(len(bio)):
        csv_writer.writerow([bio[i], followings[i], followers[i], location[i], website[i]])


