import cohere
def callAPI():
  place = input("Location: ")
  time = input("Duration: ")

  co = cohere.Client('9QeAtosokYNhPasDam5aqh4tyb16r7WUwWtEebEf') # This is your trial API key

  prompt = ("make a short %s day itinerary including specific restaurants in %s for a user interested in relaxing, tourist spots, good local food" %(time,place))
  # print(prompt)
  # prompt = ("make a %s day itinerary with specific restaurants for %s" % (time,place))

  response = co.generate(
    model='5d623c8d-7dee-4c80-9956-c1197b3898b6-ft',
    prompt= prompt,
    max_tokens=2000, #944
    temperature=0.9,
    k=0,
    stop_sequences=[],
    return_likelihoods='NONE')
  
  # print(splitByDay(response.generations[0].text))
  print(response.generations[0].text)
  return response.generations[0].text

def splitByDay(plan):
  arr = []
  start = 0

  for i in range(len(plan)):
      if plan[i:i+5] == '\nDay ':
          arr.append(plan[start:i-1])
          start = i

  arr.append(plan[start:])
  arr.pop(0)
  return arr

# def checkLocation(place):
#   co = cohere.Client('XN7jFJbkwwW4DAvC2QGNn7L9TGbYOSBjFF6W5lEB') # This is your trial API key

#   prompt = "Yes/No is %s a real location on earth?" %(place)

#   response = co.generate(
#     model='32b90b22-edf5-4c3c-a370-f38d0edb8fa6-ft',
#     prompt= prompt,
#     max_tokens=100,
#     temperature=0.5,
#     k=0,
#     stop_sequences=[],
#     return_likelihoods='NONE')
  
#   sol = response.generations[0].text

#   if ("Yes" in sol):
#     return True
  
#   return False

    
callAPI()