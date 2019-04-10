import googlemaps

def get_dic_by_key(listdic, key, value):
    for i in range(len(listdic)):
        if listdic[i][key] == value:
            return listdic[i]
    return None

def get_latlng_from_address_str(address_str):
    gmaps = googlemaps.Client(key ='AIzaSyCgsG2vhClFly8kadgTOHCX4wucOwgTiuw')
    geocode_result = gmaps.geocode(address_str)
    return [geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']]

def get_positive(number):
    if number < 0:
        return number*(-1)
    return number



def remove_left_zero(number):
    string = str(number)
    while string[0] == "0":
        string = string[1:]
    return string

def add_left_zero(number):
    if len(str(number)) == 1:
        number_str = "0" + str(number)
    else:
        number_str = str(number)
    return number_str
# Comparing two different Strings
def compare_strings(string1, string2):
    error = (levenshtein(string1.lower(), string2.lower()) - len(string1) + len(string2))/len(string2)
    print(error)
    accept = False
    if error < 0.3:
        accept = True
    return accept


def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]
