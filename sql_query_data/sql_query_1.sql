SELECT DISTINCT ctd.drink_name AS drink_name
FROM   cocktail_drinks AS ctd
       INNER JOIN cocktail_ingredients AS cti_lemon
               ON ctd.id = cti_lemon.drink_id
       INNER JOIN ingredients AS ing_lemon
               ON cti_lemon.ingredients_id = ing_lemon.id
       INNER JOIN cocktail_ingredients AS cti_whiskey
               ON ctd.id = cti_whiskey.drink_id
       INNER JOIN ingredients AS ing_whiskey
               ON cti_whiskey.ingredients_id = ing_whiskey.id
WHERE  ctd.alcoholic = "alcoholic"
       AND ing_lemon.ingredients_name LIKE "%lemon%"
       AND ing_whiskey.ingredients_name LIKE "%whiskey%"; 