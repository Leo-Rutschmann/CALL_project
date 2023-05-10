import spacy

# load pre-trained word vectors
nlp = spacy.load('en_core_web_md')


def calculateUserScore(userWord, targetWord):
    # get word vectors for userWord and targetWord
    userVec = nlp(userWord).vector
    targetVec = nlp(targetWord).vector

    # calculate cosine similarity between vectors
    dot_product = userVec.dot(targetVec)
    magnitude_user = (userVec ** 2).sum() ** 0.5
    magnitude_target = (targetVec ** 2).sum() ** 0.5
    cosine_similarity = dot_product / (magnitude_user * magnitude_target)

    # convert cosine similarity to distance score
    distance_score = 1 - cosine_similarity

    return distance_score


distance_score = calculateUserScore("cat", "dog")
distance_score = calculateUserScore("bark", "dog")
distance_score = calculateUserScore("dog", "dog")
print(abs(round(float("2"[:4]), 3)))
print(calculateUserScore("cat", "television"))
print(calculateUserScore("television", "television"))
