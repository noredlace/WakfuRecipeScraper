# Wakfu Recipe Scraper

Basic Functionality to Extract Recipes from Wakfu's Website.

Config.json is used to pass the URLs we'd like to access.

i.e. provide the URL  https://www.wakfu.com/en/mmorpg/encyclopedia/jobs/77-armorer/recipes and we will look at https://www.wakfu.com/en/mmorpg/encyclopedia/jobs/77-armorer/recipes?page=1, https://www.wakfu.com/en/mmorpg/encyclopedia/jobs/77-armorer/recipes?page=2, etc. until we don't get a page back

We then parse the Tables on the Site to extract the information for recipes

The json structure is an array of objects like so
```
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
```
We store these as JSON files for the respective professions and can be referenced by other programs

## Python Dependencies
```
pip install selenium
```
Get the chromedriver.exe off selenium's Wiki for drivers

Add the chromedriver.exe folder to your path

## Angular Site
[Github Repo](https://github.com/noredlace/wakfu-recipe-calculator)
