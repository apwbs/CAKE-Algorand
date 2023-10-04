ini_list = '[2463920186273117201 and (MANUFACTURER or SUPPLIER), 2463920186273117201 and (MANUFACTURER or (SUPPLIER and ELECTRONICS)), 2463920186273117201 and (MANUFACTURER or (SUPPLIER and MECHANICS))]'
#ini_list = '[ID, SortAs, GlossTerm],[Acronym, Abbrev],[Specs, Dates]'
# printing initialized string of list and its type
print("initial string", ini_list)
print(type(ini_list))
 
# Converting string to list
res = ini_list.strip('][').split(', ')
 
# printing final result and its type
print("final list", res)
print(type(res))

#'["ID", "SortAs", "GlossTerm"],["Acronym", "Abbrev"],["Specs", "Dates"]'