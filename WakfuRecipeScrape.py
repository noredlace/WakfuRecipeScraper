from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import sys
import json
import time

#Load JSON for Variables
with open('config.json','r') as read_file:
    data = json.load(read_file)

#config variable settings
Profession = data["Recipes"][0]["Profession"]
BaseURL = data["Recipes"][0]["URL"]

#Start Code
try:
    
    jsonList = []
    driver = webdriver.Chrome()

    i = 1

    while(i<40):
        ##We want to continuously access each incremental page until get the message that we don't have recipes anymore https://www.wakfu.com/en/mmorpg/encyclopedia/jobs/77-armorer/recipes?page=36
        url = BaseURL + "?page=" + str(i)

        
        driver.get(url)

        ##Check for Page with No Items and Exit
        ##There is probably some cleaner way to do this in Selenium than doing a Try/Catch block for this
        try:
            hasRecipes = driver.find_elements_by_xpath("//div[@id='tab1']//div[@class='ak-panel-content']")
            ##hasRecipes = driver.find_elements(By.XPATH,"//div[@id='tab1']//div[@class='ak-panel-content']")
            print(hasRecipes.text)
            print("No More Recipes found at " + url)

            driver.close()

            ##If we are at the end, dump our jsonList of all recipes to the Json File named after the Profession
            fileName = Profession + "Recipes.json"
            f = open(fileName,"w")
            f.write(json.dumps(jsonList))
            f.close()

            ##break out of our Loop and end the script
            break
        except:
            print("Recipes found at " + url)
        
        for el in driver.find_elements_by_xpath("//tr[@class='ak-bg-odd' or @class='ak-bg-even']"):
            Item = {}

            urlID = el.find_element_by_xpath(".//td[@class='img-first-column']//a").get_attribute("href")
            Item["urlID"] = urlID

            urlImage = el.find_element_by_xpath(".//td[@class='img-first-column']//a//img").get_attribute("src")
            Item["urlImage"] = urlImage

            name = el.find_element_by_xpath(".//td[2]").text
            Item["Name"] = name

            type = el.find_element_by_xpath(".//td[3]").text
            Item["Type"] = type

            recipeList = []
            for child in el.find_elements_by_xpath(".//td[4]//a"):
                childUrlID = child.get_attribute("href")

                childUrlImage = child.find_element_by_xpath(".//img").get_attribute("src")
                
                childQty = child.text

                recipeList.append({"urlID": childUrlID, "urlImage": childUrlImage, "qty": childQty})

            Item["Recipe"] = recipeList

            level = el.find_element_by_xpath(".//td[5]").text
            Item["Level"] = level

            jsonList.append(Item)

        time.sleep(2)

        ##increment to the next page
        i = i + 1

    driver.close()

    ##If we are at the end, dump our jsonList of all recipes to the Json File named after the Profession
    fileName = Profession + "Recipes.json"
    f = open(fileName,"w")
    f.write(json.dumps(jsonList))
    f.close()


except:
    print("Unexpected Error:", sys.exc_info()[0])

        

    