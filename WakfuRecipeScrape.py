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


##data = {"Recipes": [{"Profession": "Jeweler", "URL": "https://www.wakfu.com/en/mmorpg/encyclopedia/jobs/78-jeweler/recipes"}]}

#Start Code
try:

    for d in data["Recipes"]:

        Profession = d["Profession"]
        BaseURL = d["URL"]

        print('Accessing Recipes at ' + BaseURL)
    
        jsonList = []

        ##Ignore Errors from ChromeDriver that are irrelevant
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches',['enable-logging'])
        driver = webdriver.Chrome(options=options)

        i = 1

        #hardcoded for now, need to dynamically check this. max page i saw was 36, so 40 will be fine for now
        while(i<100):
            ##We want to continuously access each incremental page until get the message that we don't have recipes anymore https://www.wakfu.com/en/mmorpg/encyclopedia/jobs/77-armorer/recipes?page=36
            url = BaseURL + "?page=" + str(i)
            
            driver.get(url)

            print(url)

            ##Wait 10 seconds incase cloudflare redirect comes up. probably better way to do this
            time.sleep(10)

            ##Check for Page with No Items and Exit
            ##If element that holds "This profession does not have harvests." exists. exit the loop and continue to the next profession recipes
            hasRecipes = driver.find_elements(By.XPATH,"//div[@id='tab1' or @id='tab2']//div[@class='ak-container ak-panel']//div[@class='ak-panel-content']")
            if (len(hasRecipes) > 0):
                print("No More Recipes at " + url)
                break

            '''
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
            '''
            try:
                for el in driver.find_elements_by_xpath("//tr[@class='ak-bg-odd' or @class='ak-bg-even']"):
                    Item = {}

                    urlID = el.find_element_by_xpath(".//td[@class='img-first-column']//a").get_attribute("href")
                    Item["urlID"] = urlID
                    
                    urlArray = urlID.split('/')
                    urlArray.reverse()
                    itemIDAndName = urlArray[0].split('-')
                    itemID = itemIDAndName[0]
                    Item["ItemID"] = itemID

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

                    try:
                        level = el.find_element_by_xpath(".//td[5]").text
                        Item["Level"] = level
                    except:
                        Item["Level"] = "NULL"
                    jsonList.append(Item)
            except:
                print("No Recipes found at " + url)
            ##time.sleep(2)

            ##increment to the next page
            i = i + 1

        driver.close()

        ##If we are at the end, dump our jsonList of all recipes to the Json File named after the Profession
        fileName = "Recipes\\" + Profession + "Recipes.json"
        f = open(fileName,"w")
        f.write(json.dumps(jsonList))
        f.close()


except:
    print("Unexpected Error:", sys.exc_info()[0])

        

    