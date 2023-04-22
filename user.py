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

    def toggleType(self, typeName) -> bool:
        self.personality[typeName] = not self.personality[typeName]