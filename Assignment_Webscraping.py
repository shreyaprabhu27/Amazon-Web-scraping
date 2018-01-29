#Importing the required libraries
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

chrome_path = r"G:\Study\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)
#The below line is executed when I accessed the amazon page for the first time. Searced for "printers"
#driver.get("https://www.amazon.com/s/ref=nb_sb_noss/137-6943672-6700063?url=search-alias%3Daps&field-keywords=printer")

#Saved the file on my local too
driver.get("C:/Users/Owner/Desktop/Trinity/Amazon.com_ printer_final.html")

html = driver.page_source
soup = BeautifulSoup(html, "lxml")

#This list will store the product name and code 
productdetails = []
#This code will scrape the a tags with the relevant class attribute. The title field of the a tag contains both product name and the code.
for link in soup.findAll('a', {'class' : 'a-link-normal'}):
		titlevalue = link.get('title')
		if(titlevalue is not None):
			productdetails.append(titlevalue)


#This list will store the product price details
pricedetails = []
#This code will scrape the div and span tags with the relevant class attributes. The price for the product is available in tag - a-offscreen or a-size-base-plus a-color-secondary a-text-strike or a-size-base a-color-base. I have picked up the price in the same order. If it not available in the first tag, i checked the second and then the third. The count variable is set to 1 once we fetch the price of the product. This prevents the code from retrieving  price of the same product again. 
count = 0;
for a in soup.findAll('div', {'class' : ['a-row a-spacing-none', 'a-row a-spacing-none acs-price-row']}):
	for link in a.findAll('span',  {'class' : ['a-offscreen', 'a-size-base-plus a-color-secondary a-text-strike', 'a-size-base a-color-base']}):
		if(count == 0):
			if(link.get('class').count('a-offscreen')>= 1):
				pricedetails.append(link.get_text())
				count = 1
			elif(link.get('class').count('a-text-strike')>= 1):
				pricedetails.append(link.get_text())
				count = 1
			elif((link.get('class').count('a-size-base a-color-base') >= 1)):
				pricedetails.append("0")
				count = 1
	count = 0	
	
#Remove the unwanted field: "Sponsored" from the list
formattedpricelist = []
for a in pricedetails:
	if(a != '[Sponsored]'):
		formattedpricelist.append(a)
		
#Preparing a dictionary that contains both product and price details
result ={'Product': productdetails,'Price': formattedpricelist}

#Creating a dataframe from the dictionary
amazonqueryresults = pd.DataFrame(result)
print("Sample results\n")
print(amazonqueryresults.head(5))

#Store the dataframe in an excel sheet
amazonqueryresults.to_excel("Results.xls")
print("Complete Results are stored in file - Results.xls") 

	
