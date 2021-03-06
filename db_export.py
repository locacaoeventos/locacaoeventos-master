import os


# Para pegarmos a base de dados do sistema atual
# os.system("python manage.py dumpdata --exclude=my_admin > db.json")
# os.system("python manage.py dumpdata core.DadoError> db.json")
str_command = "python3.6 manage_production.py dumpdata "


# ======================= Models to save
str_command += "placecore.place "
str_command += "placecore.placeadditionalinformation "
str_command += "placecore.placevisualization "
str_command += "placecore.photoprovisory "
str_command += "placecore.placephoto "
str_command += "placecore.placefeature "

str_command += "placereservation.placeprice "
str_command += "placereservation.placeunavailability "
str_command += "placereservation.placereservation "

str_command += "placereview.placereview "

str_command += "buyerprofile.buyerprofile "
str_command += "buyerprofile.familymember "

str_command += "chat.message "

str_command += "sellerprofile.sellerprofile "

str_command += "auth.user "

# ======================= Models to save


str_command += " > database/db_export.json"
os.system(str_command)
