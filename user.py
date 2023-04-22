import random
import string

class User:

    personality = {
        "Thrillers": False,
        "InvisibleHopper" : False,
        "CityHustler" : False,
        "LoneWolf" : False,
        "TypicalTraveller" : False,
        "SocialMediaCrazy" : False,
        "LoveBirds" : False,
        "NatureLover" : False,
        "Foodie" : False,
        "NightOwl" : False
    }

    description = {
        "Thrillers": "adrenaline activities",
        "InvisibleHopper" : "relaxing",
        "CityHustler" : "city activities",
        "LoneWolf" : "secluded areas",
        "TypicalTraveller" : "tourist spot",
        "SocialMediaCrazy" : "picture places",
        "LoveBirds" : "romantic activities",
        "NatureLover" : "natural places",
        "Foodie" : "good local food",
        "NightOwl" : "night life"
    }

    users = {}
    userGroups = {}
    groups = {}

    def createGroup(self):
        group_name = input("Enter group name: ")

        # generate random 5-letter alphanumeric code
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

        # check if the generated code already exists
        while code in self.groups:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

        # add the new group to the dictionary
        self.groups[code] = group_name

        print(f"Group '{group_name}' has been created with code '{code}'.")

    def joinGroup(self):
        user_code = input("Enter 5-letter alphanumeric code to join group: ")

        if user_code in self.groups:
            group_name = self.groups[user_code]
            print(f"You have joined {group_name}!")
        else:
            print("Invalid code. Please try again.")


    def toggleType(self, typeName) -> bool:
        self.personality[typeName] = not self.personality[typeName]