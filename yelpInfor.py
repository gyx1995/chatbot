# search based on business name; rank; address; phone number(unknown business ID)
testresponse = {
    'alias': 'amys-ice-creams-austin-3',
    'categories': [{'alias': 'icecream', 'title': 'Ice Cream & Frozen Yogurt'},
                   {'alias': 'hotpot', 'title': 'Hot Pot'}],
    'coordinates': {'latitude': 30.2720075610766, 'longitude': -97.7544708294765},
    'display_phone': '(512) 480-0673',
    'hours': [{'hours_type': 'REGULAR',
               'is_open_now': False,
               'open': [{'day': 0,
                         'end': '0000',
                         'is_overnight': False,
                         'start': '1130'},
                        {'day': 1,
                         'end': '0000',
                         'is_overnight': False,
                         'start': '1130'},
                        {'day': 2,
                         'end': '0000',
                         'is_overnight': False,
                         'start': '1130'},
                        {'day': 3,
                         'end': '0000',
                         'is_overnight': False,
                         'start': '1130'},
                        {'day': 4,
                         'end': '0100',
                         'is_overnight': True,
                         'start': '1130'},
                        {'day': 5,
                         'end': '0100',
                         'is_overnight': True,
                         'start': '1130'},
                        {'day': 6,
                         'end': '0000',
                         'is_overnight': False,
                         'start': '1130'}]}],
    'id': 'G6H8NkJUkKAtfzn7KEb2Zg',
    'image_url': 'https://s3-media2.fl.yelpcdn.com/bphoto/O3WwHqJ6jARLGz-h8G5TEA/o.jpg',
    'is_claimed': True,
    'is_closed': False,
    'location': {'address1': '1012 W 6th St',
                 'address2': '',
                 'address3': '',
                 'city': 'Austin',
                 'country': 'US',
                 'cross_streets': '',
                 'display_address': ['1012 W 6th St', 'Austin, TX 78703'],
                 'state': 'TX',
                 'zip_code': '78703'},
    'name': "Amy's Ice Creams",
    'phone': '+15124800673',
    'photos': ['https://s3-media2.fl.yelpcdn.com/bphoto/O3WwHqJ6jARLGz-h8G5TEA/o.jpg',
               'https://s3-media2.fl.yelpcdn.com/bphoto/VmrkdYq1-BriWjqLEZ9npA/o.jpg',
               'https://s3-media3.fl.yelpcdn.com/bphoto/DGxl0TgqZmb1ST7mZAygIQ/o.jpg'],
    'price': '$$$$',
    'rating': 4.5,
    'review_count': 349,
    'transactions': [],
    'url': 'https://www.yelp.com/biz/amys-ice-creams-austin-3?adjust_creative=lhbBcUeH40MJqyrOOq4QBg&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_lookup&utm_source=lhbBcUeH40MJqyrOOq4QBg'
}


# get the business ID.
def get_id(response):
    ret = response["id"]
    return ret


# get the business address.
def get_address(response):
    ret = response["location"]["display_address"]
    return ret[0] + ret[1]


# get the business phone number.
def get_phone_num(response):
    ret = response["display_phone"]
    return ret


# # get the first i business names.
# def get_names(response, i):
#     return


# get the business name.
def get_name(response):
    ret = response["name"]
    return ret


# get the business name, return a list business name
def get_names(response):
    list_of_names = []
    businesses = response["businesses"]
    for business in businesses:
        name = get_name(business)
        list_of_names.append(name)
    return list_of_names


# get a list of the weekly business hours from Monday to Sunday, each element indicates (day,is_overnight,hours)
def get_hours(response):
    ret = []
    days = response["hours"][0]["open"]
    for day in days:
        daynum = day["day"]
        if daynum == 0:
            whichday = "Monday"
        elif daynum == 1:
            whichday = "Tuesday"
        elif daynum == 2:
            whichday = "Wednesday"
        elif daynum == 3:
            whichday = "Thursday"
        elif daynum == 4:
            whichday = "Friday"
        elif daynum == 5:
            whichday = "Saturday"
        elif daynum == 6:
            whichday = "Sunday"
        is_overnight = day["is_overnight"]
        start = day["start"][0:2] + ":" + day["start"][2:4]
        end = day["end"][0:2] + ":" + day["start"][2:4]
        hours = start + " ~ " + end
        details = (whichday, is_overnight, hours)
        ret.append(details)
    return ret


# return a list of categories, the element indicates(alias, title)
def get_categories(response):
    ret = []
    categories = response["categories"]
    for category in categories:
        ele = (category["alias"], category["title"])
        ret.append(ele)
    return ret


# return true if the business is open, otherwise false
def get_status(response):
    ret = response["hours"][0]["is_open_now"]
    return ret


# return price level, the higher the value is, the more expensive
def get_price_level(response):
    ret = len(response["price"])
    return ret


# return the rating score
def get_rating(response):
    ret = response["rating"]
    return ret


# return the number of review
def get_review_count(response):
    ret = response["review_count"]
    return ret


# get reviews

if __name__ == '__main__':
    print(get_review_count(testresponse))
    print(get_rating(testresponse))
