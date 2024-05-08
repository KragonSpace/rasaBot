from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

import requests
from ai21 import AI21Client
from ai21.models.chat import ChatMessage


# class ActionAskFirstName(Action):
#     def name(self):
#         return "action_ask_first_name"

#     def run(self, dispatcher: CollectingDispatcher, tracker, domain):
#         user_name = next(
#             (event.get("text") for event in reversed(tracker.events) if event.get("text")),
#             None
#         )
#         print(tracker.events)
#         if '!' in user_name:
#             user_name = user_name.split('!')[0]
#             print('ask user name ===== ', user_name)

#             user_name = user_name.split(',')[1]
#         print('ask2 user name = ', user_name)
        
#         dispatcher.utter_message(text=f"Hi, {user_name}, What's your last name?")
#         return []

class ActionAskLastName(Action):
    def name(self):
        return "action_ask_last_name"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # user_name = tracker.get_slot('first_name')
        user_name = next(tracker.get_latest_entity_values('PERSON'), None)
        
        if user_name is None:
            user_name = next(
                (event.get("text") for event in reversed(tracker.events) if event.get("text")),
                None
            )
        print('greet first name = ', user_name)
        
        if '!' in user_name:
            user_name = user_name.split('!')[0]
            user_name = user_name.split(',')[1]
            print('user name = ', user_name)            
        elif user_name is None:
                dispatcher.utter_message(text="Hello! again")
                return [SlotSet('awaiting_name', True)]
        
        dispatcher.utter_message(response="utter_ask_last_name", first_name=user_name.capitalize())
        return [SlotSet('first_name', user_name)]

class ActionGreetFullname(Action):
    def name(self):
        return "action_greet_fullname"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_firstname = tracker.get_slot('first_name')
        print('first name = ', user_firstname)
        user_lastname = next(tracker.get_latest_entity_values('PERSON'), None)
        if user_lastname == None:
            user_lastname = next(
                (event.get("text") for event in reversed(tracker.events) if event.get("text")),
                None
            )
        # user_lastname = tracker.get_slot('lastname')
        print('last name = ', user_lastname)
        # if user_firstname == user_lastname and user_lastname is not None:
        # #     user_firstname = ''
        if user_lastname:
            # dispatcher.utter_message(text=f'Ok, {user_firstname.capitalize()} {user_lastname.capitalize()}, Let me ask you more')
            dispatcher.utter_message(text=f'Ok, {user_firstname.capitalize()} {user_lastname.capitalize()}, What is the name of your company?')

        else:
            dispatcher.utter_message(text="Hello")
        return [SlotSet('last_name', user_lastname)]

class ActionSetCompanyName(Action):
    def name(self) -> Text:
        return "action_set_company_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        company_name = next(tracker.get_latest_entity_values("company_name"), None)
        if company_name:
            return [SlotSet("company_name", company_name)]
        else:
            company_name = next(
                (event.get("text") for event in reversed(tracker.events) if event.get("text")),
                None
            )
        # dispatcher.utter_message(response="utter_ask_company_name")
        return [SlotSet("company_name", company_name)]

class ActionAcknowledgeCompanyName(Action):
    def name(self) -> Text:
        return "action_acknowledge_company_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        company_name = tracker.get_slot("company_name")

        if company_name:
            dispatcher.utter_message(f"Got it! Your company, {company_name}, is now registered. Let me know your role at {company_name}")
        else:
            dispatcher.utter_message("Sorry, I didn't catch the name of your company.")

        return []

class ActionSetCompanyRole(Action):
    def name(self) -> Text:
        return "action_set_company_role"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        company_role = next(tracker.get_latest_entity_values("company_role"), None)
        if company_role:
            return [SlotSet("company_role", company_role)]
        else:
            company_role = next(
                (event.get("text") for event in reversed(tracker.events) if event.get("text")),
                None
            )
        # dispatcher.utter_message(response="utter_ask_company_role")
        return [SlotSet("company_role", company_role)]

class ActionAcknowledgeCompanyRole(Action):
    def name(self) -> Text:
        return "action_acknowledge_company_role"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        company_role = tracker.get_slot("company_role")

        if company_role:
            dispatcher.utter_message(f"Got it! Your company role, {company_role}, is now registered. What is your email address?")
        else:
            dispatcher.utter_message("Sorry, I didn't catch your role.")

        return []

class ActionCaptureEmail(Action):
    def name(self) -> Text:
        return "action_capture_email"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(text="Please provide your email address.")
        return []

class ActionEmailConfirmation(Action):
    def name(self) -> Text:
        return "action_email_confirmation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        email = tracker.get_slot("email")
        dispatcher.utter_message(text=f"Thank you! Your email address ({email}) has been captured.")
        return []