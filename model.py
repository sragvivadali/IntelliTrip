import cohere
co = cohere.Client('XN7jFJbkwwW4DAvC2QGNn7L9TGbYOSBjFF6W5lEB') # This is your trial API key

place = input("Location: ")
time = input("Duration: ")

prompt = ("make a short bullet point list itinerary for %s for %s days. List the hotels, restaurants and attractions \n" % (place,time))

response = co.generate(
  model='32b90b22-edf5-4c3c-a370-f38d0edb8fa6-ft',
  prompt= prompt,
  max_tokens=944,
  temperature=0.9,
  k=0,
  stop_sequences=[],
  return_likelihoods='NONE')

print(prompt)
print('Prediction: {}'.format(response.generations[0].text))