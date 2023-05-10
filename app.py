from flask import Flask, render_template, redirect, request
import os

import db
from auth import auth
import random
import re

from static.user_score import calculateUserScore
from static.corpus import corpus
from static.labeled_words import labeled_words

corpusByLevels = {}
corpusByWords = {}
condensed = []
condensedAll = []
limit = 3

def makeCorpusByWords():
    for word in labeled_words:
        w = word['word']
        level = word['level']
        pos = word['POS']
        # if level == "A2":
        for sentence in corpus:
            if re.search('\\b' + w + '\\b', sentence['sentence']):
                if w not in corpusByWords:
                    corpusByWords[w] = {'all':[]}
                if level not in corpusByWords[w]:
                    corpusByWords[w][level] = []
                # print("yes, " + target + " => " + sentence)
                sent = sentence['sentence'].replace(w, '_____')
                if sentence['level'] == level:
                    corpusByWords[w][level].append(sent)
                corpusByWords[w]['all'].append(sent)

def getQuestions(target, level, amount=4):
    if level == 'Shuffle all levels':
        level = 'all'
    if target in corpusByWords:
        if level in corpusByWords[target]:
            sentences = corpusByWords[target][level]
            random.shuffle(sentences)
            return sentences[:amount]
        else:
            return []
    else:
        return []

def getTargetWord(level):
    corpusKeys = list(corpusByWords.keys())
    # filtered = [target['word'] if (level == target['level'] and target['word'] in corpusKeys) else '' for target in labeled_words]
    filtered = []
    for target in labeled_words:
        if target['word'] in corpusKeys:
            if target['level'] == level:
                filtered.append(target['word'])
                # print("new word => " + target['word'])
    w = random.choice(filtered)
    # print("w: " + w)
    return w

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/', methods=['GET', 'POST'])
    def start():
        levels = ['A1','A2','B1','B2','C1','C2','Shuffle all levels']
        return render_template('pages/start.html', levels=levels)

    @app.route('/question', methods=['GET', 'POST'])
    def question():
        # if request.method == 'POST':
            # comes from the submit-button, meaning that a user has given an answer
        # else:
        data = request.args
        content = 'test content'
        questions = []
        suggestions = []
        target = None
        finished = False
        thisRoundPoints = 0


        guessed = 'guess' in data.keys()
        nextGuess = 'proceed' in data.keys()

        # process and keep track
        level = data['level']

        # update target word and question sentences
        enough = False
        for i in range(100):
            if not enough:
                target = getTargetWord(level)
                questions = getQuestions(target, level)
                print(len(questions))
                if len(questions) > 2:
                    enough = True
        suggestions = ['run', 'go']

        if ('currentPoints' in data):
            currentPoints = float(data['currentPoints'])
            currentPoints = round(currentPoints)
        else:
            currentPoints = 0
        if ('status' in data):
            status = int(data['status'])
            if int(status) >= int(limit):
                finished = True
            else:
                status += 1
                finished = False
        else:
            status = 1
        if ('finish' in data):
            finished = True

        # if there is a guess, update the user score
        if 'guess' in data:
            # count points
            count = calculateUserScore(data['guess'], data['target'])
            thisRoundPoints = abs(round(float(str(count)[:4]), 3))
            thisRoundPoints = thisRoundPoints*100
            currentPoints += thisRoundPoints
        #     nextGuess = False
        # else:
        #     nextGuess = True

        return render_template('pages/question.html',
                                data=data,
                                level=level,
                                status=status,
                                thisRoundPoints=thisRoundPoints,
                                currentPoints=currentPoints,
                                guessed=guessed,
                                content=content,
                                questions=questions,
                                suggestions=suggestions,
                                finished=finished,
                                limit=limit,
                                target=target,
                                nextGuess=nextGuess)

    db.init_app(app)
    app.register_blueprint(auth.bp)

    # print("making corpus by words")
    makeCorpusByWords()
    # print("done making corpus by words")
    # print()
    # print()
    # print(corpusByWords[list(corpusByWords.keys())[0]])
    for word, stuff in corpusByWords.items():
        totalLen = 0
        for level, sents in stuff.items():
            totalLen += len(sents)
            if len(sents) > 2:
                # print(word + " => " + level)
                condensed.append(word)
        if totalLen > 2:
            condensedAll.append(word)
    # print()
    # print()
    # print(len(condensed))
    # print(len(condensedAll))

    # for sentence in corpus:
    #     if sentence['level'] not in corpusByLevels:
    #         corpusByLevels[sentence['level']] = []
    #     corpusByLevels[sentence['level']].append({'sentence': sentence['sentence']})

    return app