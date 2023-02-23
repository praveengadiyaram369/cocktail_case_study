WITH temp_data
     AS (SELECT DISTINCT ctd.drink_name            AS drink_name,
                         Count(DISTINCT cti.ingredients_id) AS ing_count
         FROM   cocktail_drinks AS ctd
                INNER JOIN cocktail_ingredients AS cti
                        ON ctd.id = cti.drink_id
         GROUP  BY drink_name)
SELECT drink_name
FROM   temp_data
WHERE  ing_count = (SELECT Max(ing_count)
                    FROM   temp_data); 