WITH temp_data
     AS (SELECT ctd.drink_name                                           AS
                drink_name,
                ( cti.min_quantity * mc.conversion_multiplying_factor )  AS
                   min_quantity_gm,
                ( cti. max_quantity * mc.conversion_multiplying_factor ) AS
                   max_quantity_gm
         FROM   cocktail_drinks AS ctd
                INNER JOIN cocktail_ingredients AS cti
                        ON ctd.id = cti.drink_id
                INNER JOIN ingredients AS ing
                        ON cti.ingredients_id = ing.id
                INNER JOIN measurement_units AS mu_from
                        ON cti.measurement_unit_id = mu_from.id
                INNER JOIN measurement_conversion AS mc
                        ON mu_from.id = mc.measurement_from_id
                INNER JOIN measurement_units AS mu_to
                        ON mc.measurement_to_id = mu_to.id
         WHERE  ing.ingredients_name = "sambuca"
                AND mu_to.measurement_name = "gr"
                AND mu_from.measurement_name IN ( "oz", "gr"))
SELECT drink_name
FROM   temp_data
WHERE  max_quantity_gm < 15; 