/*
JSON Structure:

[{
    "urlID" = "en/...",
    "urlImage" = "string",
    "Name" = "string",
    "Type" = "string",
    "Recipe" = [
        {
            "urlID" = "en/...",
            "urlImage" = "string",
            "qty" = "string",
        },
        {
            "urlID" = "en/...",
            "urlImage" = "string",
            "qty" = "string",
        }
    ]
    "Level" = "string"
},{
    "urlID" = "en/...",
    "urlImage" = "string",
    "Name" = "string",
    "Type" = "string",
    "Recipe" = [
        {
            "urlID" = "en/...",
            "urlImage" = "string",
            "qty" = "string",
        },
        {
            "urlID" = "en/...",
            "urlImage" = "string",
            "qty" = "string",
        }
    ]
    "Level" = "string"
}]

*/

this.document.location = "https://www.wakfu.com/en/mmorpg/encyclopedia/jobs/77-armorer/recipes?page=1"

setTimeout(getItemRecipes(), 10000)

function getItemRecipes(){

    var items = [];

    $('.ak-table.ak-responsivetable > tbody > tr').each(function() {
        var item = new Object();
        var recipe = new Object();

        $(this).each(function() {
            
            //0 1st Column. urlID, urlImage
            var urlCol = $(this).children()[0];
            item.urlID = $(urlCol).children().attr("href");
            item.urlImage = $(urlCol).children().children().attr("src");

            //1 2nd Column. Name
            urlCol = $(this).children()[1];
            item.name = $(urlCol).children().text();

            //2 3rd Column. Type
            urlCol = $(this).children()[2];
            item.type = $(urlCol).closest('td').text();

            var recipes = [];
            //3 4th Column. Recipes of child Objects of urlID, urlImage, quantity
            urlCol = $(this).children()[3];
            $(urlCol).children('a').each(function () {
                var recipe = new Object();
                recipe.quantity = $(this).text();
                recipe.urlID = $(this).attr("href"); 
                recipe.urlImage = $(this).children().attr("src");
                recipes.push(recipe);
            })
            item.recipes = recipes;


            //4 5th Column. Level
            urlCol = $(this).children()[4];
            item.level = $(urlCol).closest('td').text();

            //console.log(item);
            items.push(item);
        });
    });

    JSON.stringify(items);
}
