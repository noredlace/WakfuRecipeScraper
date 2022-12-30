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

##data = {"Recipes": [{"Profession": "Lumberjack", "URL": "https://www.wakfu.com/en/mmorpg/encyclopedia/jobs/71-lumberjack/recipes"}]}

#Start Code
try:

    ##Any unknown child recipe IDs should default to a negative number. decrement the number each time its used to keep the ID unique 
    ##This is typical of Recipes they have where it is not craftable anymore/special event but they still have it on the site
    unknownChildID = -1

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
            ##time.sleep(10)

            ##Check for Page with No Items and Exit
            ##If element that holds "This profession does not have harvests." exists. exit the loop and continue to the next profession recipes
            hasRecipes = driver.find_elements(By.XPATH,"//div[@id='tab1' or @id='tab2']//div[@class='ak-container ak-panel']//div[@class='ak-panel-content']")
            if (len(hasRecipes) > 0):
                print("No More Recipes at " + url)
                break

            '''
            Sample Json Array (ItemID of -1 means we couldn't find anything)
            [
                {
                    "ItemURL": "https://www.wakfu.com/en/mmorpg/encyclopedia/consumables/10374-howin-treat",
                    "ItemID": 10374,
                    "ItemImageURL": "https://static.ankama.com/wakfu/portal/game/item/42/26610374.w40h40.png",
                    "Name": "Al Howin's Treat",
                    "Type": "Food",
                    "Recipe": [
                        {
                            "ItemURL": "https://www.wakfu.com/en/mmorpg/encyclopedia//-",
                            "ItemID": -1,
                            "ItemImageURL": "https://static.ankama.com/wakfu/portal/game/item/21/.png",
                            "Name": "",
                            "Quantity": 1
                        },
                        {
                            "ItemURL": "https://www.wakfu.com/en/mmorpg/encyclopedia/resources/2340-bucket-o-water",
                            "ItemID": 2340,
                            "ItemImageURL": "https://static.ankama.com/wakfu/portal/game/item/21/2632340.png",
                            "Name": "Bucket O Water",
                            "Quantity": 1
                        },
                        {
                            "ItemURL": "https://www.wakfu.com/en/mmorpg/encyclopedia/resources/10375-piece-pumpkwin",
                            "ItemID": 10375,
                            "ItemImageURL": "https://static.ankama.com/wakfu/portal/game/item/21/26010375.png",
                            "Name": "Piece Pumpkwin",
                            "Quantity": 1
                        }
                    ],
                    "Level": 0
                }
            ]
            '''

            try:
                for el in driver.find_elements_by_xpath("//tr[@class='ak-bg-odd' or @class='ak-bg-even']"):
                    Item = {}

                    urlID = el.find_element_by_xpath(".//td[@class='img-first-column']//a").get_attribute("href")
                    Item["ItemURL"] = urlID
                    
                    urlArray = urlID.split('/')
                    urlArray.reverse()
                    itemIDAndName = urlArray[0].split('-')
                    itemID = itemIDAndName[0]
                    try:
                        Item["ItemID"] = int(itemID)
                    except:
                        Item["ItemID"] = unknownChildID
                        unknownChildID -= 1

                    urlImage = el.find_element_by_xpath(".//td[@class='img-first-column']//a//img").get_attribute("src")
                    Item["ItemImageURL"] = urlImage

                    name = el.find_element_by_xpath(".//td[2]").text
                    Item["Name"] = name

                    type = el.find_element_by_xpath(".//td[3]").text
                    Item["Type"] = type

                    recipeList = []
                    for child in el.find_elements_by_xpath(".//td[4]//a"):
                        childUrlID = child.get_attribute("href")

                        childUrlIDArray = childUrlID.split('/')
                        childUrlIDArray.reverse()
                        childItemIDAndNameArray = childUrlIDArray[0].split('-')

                        if len(childItemIDAndNameArray) > 0:
                            childID = childItemIDAndNameArray[0]

                            if (childID.strip() == ''):
                                childID = unknownChildID
                                unknownChildID -= 1
                                childName = "Unknown(" + str(unknownChildID) + ")"
                            else: 
                                childName = ""
                                for childElement in range (1, len(childItemIDAndNameArray)):
                                    childName = childName + ' ' + childItemIDAndNameArray[childElement].capitalize()
                            
                                childName = childName.strip()
                        else:
                            childID = unknownChildID
                            unknownChildID -= 1
                            childName = "Unknown(" + str(unknownChildID) + ")"

                        childUrlImage = child.find_element_by_xpath(".//img").get_attribute("src")
                        
                        ##Ankama has the Display Text as "x23". Strip out the X
                        ##They also have some expander pages that prevents me from getting it without doing this odd innerHTML array
                        childQtyArray = child.get_attribute("innerHTML").split(' ')
                        childQtyArray.reverse()
                        childQty = (childQtyArray[0]).replace("x","").strip()

                        recipeList.append({"ItemURL": childUrlID, "ItemID": int(childID), "ItemImageURL": childUrlImage, "Name": childName, "Quantity": int(childQty)})


                    Item["Recipe"] = recipeList

                    try:
                        level = (el.find_element_by_xpath(".//td[5]")).get_attribute("innerHTML")
                        Item["Level"] = int(level)
                    except:
                        Item["Level"] = -1
                    jsonList.append(Item)
            except:
                print("Error of Recipes found at " + url)
            ##time.sleep(2)

            ##increment to the next page
            i = i + 1

        driver.close()

        ##If we are at the end, dump our jsonList of all recipes to the Json File named after the Profession
        fileName = "Recipes\\" + Profession + ".json"
        f = open(fileName,"w")
        f.write(json.dumps(jsonList))
        f.close()

except:
    print("Unexpected Error:", sys.exc_info()[0])