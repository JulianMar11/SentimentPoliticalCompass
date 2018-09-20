#Requires PACKAGE: pip install --upgrade watson-developer-cloud


import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, EntitiesOptions, KeywordsOptions
import time
import sys

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username='YOURUSERNAME',
  password='YOURPASSWORD',
  version='2018-03-16')


def getsentiment(text):
    response = natural_language_understanding.analyze(
    text=text,
    features=Features(
      entities=EntitiesOptions(
        emotion=True,
        sentiment=True,
        limit=2),
      keywords=KeywordsOptions(
        emotion=True,
        sentiment=True,
        limit=2)))
    return response



errorcounter = 0

def getsentimentfromUrl(url):
    global errorcounter
    try:
        response = natural_language_understanding.analyze(
        url=url,
        language="de",
        return_analyzed_text=True,
        features=Features(
          entities=EntitiesOptions(
            sentiment=True)))
        errorcounter = max(errorcounter - 0.2, 0)
        return response, False, errorcounter
    except:
        print("WATSON API has internal server error, waiting for 3 seconds and retry")
        time.sleep(3)
        try:
            response = natural_language_understanding.analyze(
            url=url,
            language="de",
            return_analyzed_text=True,
            features=Features(
              entities=EntitiesOptions(
                sentiment=True)))
            return response, False, errorcounter
        except:
            errorcounter += 1
            print("WATSON API has internal server error")
            print(errorcounter)
            return None, True, errorcounter
