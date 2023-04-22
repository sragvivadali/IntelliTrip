import requests
import json

url = "https://gpt-chatbotapi.p.rapidapi.com/ask"

headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "1245c0d08cmsh6048f1f2b40e429p1f824ejsnda64bb5ace07",
	"X-RapidAPI-Host": "gpt-chatbotapi.p.rapidapi.com"
}

promptInput = input("Where do you want to visit? ")
prompt = "Things you must do at " + promptInput
payload = {"query": prompt}

dataCity = requests.request("POST", url, json=payload, headers=headers)

json_txt_city = dataCity.text

data = json.loads(json_txt_city)
response = data['response']

promptIt = "Given these locations, make a detailed day by day itinerary for a $500 budget per day while including resturants and hotel: \n" + response
payload = {"query": promptIt}

dataPlan = requests.request("POST", url, json=payload, headers=headers)

json_txt = dataPlan.text

dataIt = json.loads(json_txt)
response = dataIt['response']

print(response)