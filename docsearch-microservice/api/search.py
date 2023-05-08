import os
from flask_injector import inject
from api.esclient import *

qa = EsClient()

def badreq():
    return 'Bad request', 400

@inject
def search(user_payload):
    if user_payload.get('question') == None:
        return badreq()

    answer = qa.query(user_payload['question'])
    retval = {
        "question" : user_payload['question'],
        "answer" : answer
    }
    return retval

