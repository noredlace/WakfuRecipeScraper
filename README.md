# Wakfu Recipe Scraper

Basic Functionality to Extract Recipes from Wakfu's Website.

Config.json is used to pass the URLs we'd like to access.

i.e. provide the URL  https://www.wakfu.com/en/mmorpg/encyclopedia/jobs/77-armorer/recipes and we will look at https://www.wakfu.com/en/mmorpg/encyclopedia/jobs/77-armorer/recipes?page=1, https://www.wakfu.com/en/mmorpg/encyclopedia/jobs/77-armorer/recipes?page=2, etc. until we don't get a page back

We then parse the Tables on the Site to extract the information for recipes

The json structure is an array of objects like so

[{
    "urlID": "/en/mmorpg/encyclopedia/resources/18785-coarse-plate",
    "urlImage": "https://static.ankama.com/wakfu/portal/game/item/42/57518785.w40h40.png",
    "name": "Coarse Plate",
    "type": "Armorer Components",
    "recipes": [
      {
        "quantity": " x5",
        "urlID": "/en/mmorpg/encyclopedia/resources/1846-iron-ore",
        "urlImage": "https://static.ankama.com/wakfu/portal/game/item/21/3011846.png"
      },
      {
        "quantity": " x5",
        "urlID": "/en/mmorpg/encyclopedia/resources/1846-iron-ore",
        "urlImage": "https://static.ankama.com/wakfu/portal/game/item/21/3011846.png"
      }
    ],
    "level": "0"
  }]

We store these as JSON files for the respective professions and can be referenced by other programs

Python Dependencies

python -m pip install requests

python -m pip install bs4

python -m pip install cookiejar
