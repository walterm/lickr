# -*- coding: utf-8 -*-
# Script to load in all the questions into MongoDB.

from pymongo import MongoClient

# Setting up the Mongo connection
client = MongoClient()

# The collection for the questions
db = client["lickr"]
questions_collection = db["questions"]

questions = [
    [1, "Pick a person in camo.", "11.jpg", "12.jpg"],
    [2, "Pick the artsier person.", "22.jpg", "24.jpg"],
    [3, "Pick a sad image.", "23.jpg", "28.jpg"],
    [4, "Which face is more dramatic?", "3.jpg", "6.jpg"],
    [5, "Pick a pair of people.", "31.jpg", "32.jpg"],
    [6, "What does your current relationship status look like?", "5.jpg", "4.jpg"],
    [7, "Which is more 'WTF'?", "19.jpg", "10.jpg"],
    [8, "Pick a rainy day.", "39.jpg", "40.jpg"],
    [9, "Which looks more like your dream vacation?", "37.jpg", "38.jpg"],
    [10, "Pick a sunset portrait.", "34.jpg", "35.jpg"],
    [11, "Who’s selfie game is stronger?", "41.jpg", "40.jpg"]
]

def make_question_object(question):
    q_obj = {}
    q_obj["_id"] = question[0]
    q_obj["text"] = question[1]
    q_obj["image1"] = question[2]
    q_obj["image2"] = question[3]
    return q_obj

for question in questions:
    q_obj = make_question_object(question)
    questions_collection.insert(q_obj)
