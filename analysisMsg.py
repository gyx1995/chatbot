from rasa_nlu.model import Interpreter
import json


def get_msg(message):
    return message


# Given: a message
# Return: the interpreted results in Json format
def interpret_msg(message):
    msg = get_msg(message);
    interpreter = Interpreter.load("./rasa_nlu/models/current/nlu")
    result = interpreter.parse(msg)
    return result


# Given: a message
# Return: intent only if the confidence is above 70;
#         if there is no intent, return "None"
def get_intent(result_js):
    conf = result_js["intent"]["confidence"]
    if conf >= 0.7:
        intent = result_js["intent"]["name"]
        return intent
    else:
        return "None"


# Given: a message
# Return: a list of entities and values, only if the confidence is above 70
#         if there is no entities, return "None"
def get_entities(result_js):
    list_of_entities = []
    entities = result_js["entities"]
    if not entities:
        return "None"
    for entity in entities:
        if entity["confidence"] >= 0.20:
            details = (entity["entity"], entity["value"])
            list_of_entities.append(details)
        include_entities = []
    values = []
    for ent in list_of_entities:
        entity, value = ent
        include_entities.append(entity)
        values.append(value)
    ents = dict.fromkeys(include_entities)
    for i in range(len(include_entities)):
        if ents[include_entities[i]] is not None:
            ents[include_entities[i]] = str(ents[include_entities[i]]) + "|" + values[i]
        else:
            ents[include_entities[i]] = values[i]
    return ents




# print(interpret_msg("Does {Dumpling House} offer italian dishes"))
# print(interpret_msg("opening hour"))
# print(interpret_msg("address"))
# print(interpret_msg("hours"))
# print(interpret_msg("rating"))




