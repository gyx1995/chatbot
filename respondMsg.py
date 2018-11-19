import responseDic
import analysisMsg
import random
from yelpapi import YelpAPI
import yelpInfor
import re
import time
import datetime
from time import strptime

API_KEY = "7nLCu03yUmYF9gyr-zpj0tmp2mpRrufvXS_2huemBZUuLjdqyEuEMdjSSiHPFj0HEqB" \
          "-H4kVRq_b5ZFbF3vfhrUgMBMSPYcJ3BZUJYkf_f0HlDbYVN2S1e6hZ6XgW3Yx "
yelp_api = YelpAPI(API_KEY)

# global variables
location = "Vancouver, BC, Canada"
category = None
time_t = None
priceLevel = None
# the restaurants that is talking about most recently
talking_restaurants = []

num_visited_rest = 0
list_restaurants = []
dict_restaurants = {}
# the id of the restaurant that is being asked
info_rest_id = ""
# store the yelp Info
yelp_Info = {}

# day = None
# date = None
# status = None
# rank = None

# current state
STATE = 0
# initial state
INIT = 0
# restaurant_search state
RESTA_SE = 1
# refused_restaurant_research state(since the previous search is refused)
REFUSED_RESTA_SE = 2
# restaurant_info
RESTA_INF = 3
# restaurant_info (before change the state to RESTA_INF confirm with user)
RESTA_BEINF = 4
# end
END = 5

# after searching pick one of them
PICK_RESTA = 6

# ask if to restart the search
ASK_RESTA_SE = 7

# Define the policy rules
policy_rules = {
    (INIT, "restaurant_search"): (RESTA_SE, responseDic.responses["restaurant_search"]),
    (INIT, "restaurant_info"): (RESTA_INF, responseDic.responses["restaurant_info"]),

    (RESTA_SE, "affirm"): (PICK_RESTA, ["ok, which one do you want to know more about? Please tell me its name!"]),
    (RESTA_SE, "restaurant_info"): (RESTA_INF, responseDic.responses["restaurant_info"]),
    (RESTA_SE, "restaurant_search"): (ASK_RESTA_SE, ["Do you want to start a new search?"]),
    (RESTA_SE, "goodbye"): (INIT, ["OK, bye"]),
    (RESTA_SE, "None"): (RESTA_SE, ["Sorry, I do not understand you. Do you like restaurants I showed?"]),
    (RESTA_SE, "thank"): (INIT, ["No problem"]),
    (RESTA_SE, "refuse"): (REFUSED_RESTA_SE, ["how about {}"]),

    (RESTA_INF, "restaurant_info"): (RESTA_INF, responseDic.responses["restaurant_info"]),
    (RESTA_INF, "restaurant_search"): (ASK_RESTA_SE, ["Do you want to start a new search?"]),
    (RESTA_INF, "refuse"): (RESTA_INF, ["why you are refusing?"]),
    (RESTA_INF, "goodbye"): (INIT, ["OK, bye"]),
    (RESTA_INF, "thank"): (INIT, ["No problem"]),
    (RESTA_INF, "None"): (RESTA_INF, ["Sorry, I do not understand you. I only know its address, phone number, rating and hours"]),

    (PICK_RESTA, "None"): (RESTA_INF, ["No problems! what information do you want?"]),
    (PICK_RESTA, "restaurant_search"): (ASK_RESTA_SE, ["Do you want to start a new search?"]),

    # (RESTA_BEINF, "None"): (RESTA_INF, responseDic.responses["restaurant_info"]),

    (REFUSED_RESTA_SE, "affirm"): (RESTA_INF, ["ok, what info do you want know more about it?"]),
    (REFUSED_RESTA_SE, "restaurant_search"): (ASK_RESTA_SE, ["Do you want to start a new search?"]),
    (REFUSED_RESTA_SE, "refuse"): (REFUSED_RESTA_SE, ["how about {}"]),

    (ASK_RESTA_SE, "affirm"): (INIT, ["OK, what can I do for you?"]),
    (ASK_RESTA_SE, "refuse"): (RESTA_SE, responseDic.responses["restaurant_search"]),
    (ASK_RESTA_SE, "None"): (INIT, "Sorry, I got lost. Let's restart. so What can I do for you ?"),
    (ASK_RESTA_SE, "restaurant_search"): (INIT, ["OK, Let's restart. so What can I do for you ?"]),

}


def renew_parameters():
    global STATE
    global location
    global category
    global time_t
    global priceLevel
    global list_restaurants
    global num_visited_rest
    global info_rest_id
    global yelp_Info
    # print("renew_parameters is called")
    # global day
    # global date
    # global status
    # global rank
    STATE = INIT
    location = "Vancouver, BC, Canada"
    category = None
    priceLevel = None
    time_t = None
    list_restaurants = []
    num_visited_rest = 0
    talking_restaurants.clear()
    dict_restaurants.clear()
    info_rest_id = ""
    yelp_Info = {}

    # day = " "
    # date = " "
    # status = " "
    # rank = " "


def build_dict(yelp_info):
    global dict_restaurants
    businesses = yelp_info["businesses"]
    for business in businesses:
        name = yelpInfor.get_name(business)
        re_id = yelpInfor.get_id(business)
        dict_restaurants[name] = re_id
    return dict_restaurants


def find_restaurants():
    global dict_restaurants
    yelp_info = yelp_api.search_query(term="restaurants", open_at=time_t, categories=category,
                                      price=priceLevel,
                                      location=location, sort_by="rating")
    dict_restaurants = build_dict(yelp_info)
    # print(yelp_info)
    return yelp_info


def get_restaurant_info(entities):
    return "get_restaurant_info is called"


# return a list of restaurants according to the given entities
def do_restaurant_search(entities):
    yelp_info = find_restaurants()
    list_of_restaurant = yelpInfor.get_names(yelp_info)
    return list_of_restaurant


# check if the entities are in right format
# return "true", if the entities are in right format
#        "false", otherwise
def check_entities(entities):
    if "time" in entities:
        time_value = entities["time"]
        regex = r"^([01]\d|2[0-3]):([0-5]\d)$"
        if not re.search(regex, time_value):
            return "Please give me a specific time point, and it must be in 24 hour format, such as 14:30 and 06:45"
    return "true"


# sign the entity value to the corresponding global var
def sign_entities(entities):
    global location
    global category
    global time_t
    global priceLevel
    # global day
    # global date
    # global status
    # global rank
    if "location" in entities:
        location = entities["location"] + " BC, Canada"
    if "category" in entities:
        category = entities["category"]
    if "priceLevel" in entities:
        value = entities["priceLevel"]
        if value in ["high", "expensive"]:
            priceLevel = "3"
        elif value == "cheap":
            priceLevel = "1"
        else:
            priceLevel = "2"
    if "time" in entities:
        time_value = entities["time"]
        now = str(datetime.datetime.now())
        regex = r"\d{4}-\d{2}-\d{2}"
        match = re.search(regex, now)
        date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()
        mytm = str(date) + " " + time_value
        fmt = "%Y-%m-%d %H:%M"
        epochDate = int(time.mktime(time.strptime(mytm, fmt)))
        time_t = epochDate
    # print(location)
    # print(category)
    # print(time_t)
    # print(priceLevel)


def set_info_rest_id(message, intent):
    global info_rest_id
    global STATE
    if STATE == REFUSED_RESTA_SE and intent == "affirm":
        info_rest_id = dict_restaurants[talking_restaurants[0]]
    elif message in dict_restaurants and (intent == "restaurant_info" or intent == "None"):
        info_rest_id = dict_restaurants[message]


def find_info(info_key):
    # print("rest id: " + info_rest_id)
    global yelp_Info
    if yelp_Info == {}:
        yelp_Info = yelp_api.business_query(id=info_rest_id)
    if info_key == "phone number":
        info_value = yelpInfor.get_phone_num(yelp_Info)
    elif info_key == "address":
        info_value = yelpInfor.get_address(yelp_Info)
    elif info_key == "category":
        info_value = yelpInfor.get_categories(yelp_Info)
    elif info_key == "hours":
        info_value = yelpInfor.get_hours(yelp_Info)
    elif info_key == "rating":
        info_value = str(yelpInfor.get_rating(yelp_Info)) + "/5"
    return info_value


def advanced_intent(message, intent, entities):
    global policy_rules
    global STATE
    global list_restaurants
    global num_visited_rest
    global info_rest_id
    global dict_restaurants

    if STATE == INIT:
        renew_parameters()

    if check_entities(entities) != "true":
        return check_entities(entities)
    sign_entities(entities)
    result = "hmmm, I did not expect that"
    # adjust intent
    # print("dict_restaurants: " + str(dict_restaurants))
    if message in dict_restaurants and intent == "restaurant_search":
        intent = "None"
    set_info_rest_id(message, intent)
    # print("old state: " + str(STATE))
    # print("current intent: " + intent)
    # print("current entities: " + str(entities))
    # print("current info_rest_id: " + str(info_rest_id))
    try:
        STATE, response_list = policy_rules[(STATE, intent)]
    except:
        return result
    # print("new state: " + str(STATE))
    if STATE == RESTA_SE:
        if intent == "None":
            result = response_list[0]
        else:
            restaurants = do_restaurant_search(entities)
            list_restaurants = restaurants
            n = min(len(restaurants), 3)
            num_visited_rest = n
            talking_restaurants.clear()
            for i in range(n):
                talking_restaurants.append(restaurants[i])
            result = response_list[n].format(*restaurants)
    elif STATE == REFUSED_RESTA_SE:
        num_visited_rest += 1
        if num_visited_rest < len(list_restaurants):
            talking_restaurants.clear()
            talking_restaurants.append(list_restaurants[num_visited_rest])
            result = response_list[0].format(list_restaurants[num_visited_rest])
        else:
            result = "sorry, those are all I found. Let's restart!"
            renew_parameters()
            return result

    elif STATE == RESTA_INF and intent == "restaurant_info":
        regex = r"\((.*?)\)"
        # print("Inside State = RESTA_INF; intent == restaurant_info")
        if re.search(regex, message):
            # print("regex matches")
            match = re.search(regex, message)
            talking_restaurants.clear()
            talking_restaurants.append(match.group(1))
            # print("restaurant name: " + match.group(1))
            # print(" talking rest and location: " + talking_restaurants[0] + location)
            response = yelp_api.search_query(term=talking_restaurants[0], location=location)
            if response["total"] == 0:
                result = "sorry, I did not find anything that matches"
                return result
            # change the value of num_visited_rest = 0 & list_restaurants = [] also need to store the rest_id, and ask if list_restaurants[0] is what user wants
            list_restaurants = yelpInfor.get_names(response)
            dict_restaurants = build_dict(response)
            if num_visited_rest < len(list_restaurants):
                result = "Do you mean " + list_restaurants[num_visited_rest] + "?"
                talking_restaurants.clear()
                talking_restaurants.append(list_restaurants[num_visited_rest])
                STATE = REFUSED_RESTA_SE
            else:
                result = "sorry, I only found those. Let's restart!"
                renew_parameters()
                return result
        else:
            # print("regex does not match")
            if info_rest_id != "":
                result = "hmm, you got me. I don't know what do say. But I can help you find a place to eat."
                if "info" in entities:
                    valid_info_key = ["hours", "rating", "address", "phone number"]
                    info_key = entities["info"]
                    if info_key in valid_info_key:
                        if "|" in info_key:
                            result = "sorry, I can only tell you one at a time"
                        else:
                            info_value = find_info(info_key)
                            # print("info_value: " + info_key)
                            if info_value == "":
                                result = "sorry, I did not know its {}".format(info_key)
                            else:
                                result = response_list[0].format(info_key, info_value)
                else:
                    result = "oh, sorry I don't know. I only know its address, phone number, rating and hours"
            else:
                renew_parameters()
                result = "Interesting... What can I do for you? Tell me the restaurant you want to discover. Please put restaurant name inside a parentheses"
    else:
        result = response_list[0]
    if result == "hmmm, I did not expect that":
        renew_parameters()
    return result


def respond(message):
    if message == "":
        return "you need to say something, so I can help you"
    result = analysisMsg.interpret_msg(message)
    regex = r"^(N|n)(O|o)\b"
    if not re.search(regex, message):
        intent = analysisMsg.get_intent(result)
    else:
        intent = "refuse"
    simple_intent = ["None", "affirm", "goodbye", "greet", "thank", "refuse"]
    # print("intent and entities " + intent)
    if STATE == INIT and intent in simple_intent:
        response = random.choice(responseDic.responses[intent])
        return response
    entities = analysisMsg.get_entities(result)

    response = advanced_intent(message, intent, entities)
    return str(response)

# print(respond("find me some restaurants to eat at 03:10 in vancouver"))
