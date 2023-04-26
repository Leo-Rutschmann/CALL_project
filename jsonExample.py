import json

### writing JSON:
# simple python dictionary for one sentence:
sentenceObject = {'sentence': 'This is a test sentence', 'level':'A2'}
# to generate the json as a string:
sentenceJsonString = json.dumps(sentenceObject)

# python list with dictionaries inside = our corpus
corpus = [
    sentenceObject,
    {'sentence': 'Another sentence! nice', 'level':'B1'}
]
# and generate the string again:
corpusJsonString = json.dumps(corpus) # this string now contains our whole corpus in a nice format

# we can now write these strings to a file and voilà, we have a corpus file!
# OR we can load our json strings into Python objects again:

### loading JSON:
# load the json string into a Python object:
pythonObject = json.loads(sentenceJsonString)

# the result is a Python dictionary and can easily be accessed that way:
print("Test sentence:")
print(pythonObject["sentence"] + ", " + pythonObject["level"])

# the same goes for the "corpus":
corpusObject = json.loads(corpusJsonString)

# now our result is a list, so we can iterate over it:
print("\n")
print("Test whole corpus:")
for sentence in corpusObject:
    print(sentence["sentence"] + ", " + sentence["level"])