import watsonsentiment as Watson
import os
import csv
import matching
import json
import uuid
import sys
import smtplib


pathName = os.getcwd()

filenames = ['fr']

inputpath = pathName + "/Input"
outputpath = pathName + "/Output/"

articlelist = []
sentimentlist = []


def sentTerminationMail(message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("YOURMAIL", "YOURPASSWORD")
    server.sendmail("YOURMAIL", "YOURDESTINATIONMAIL", message)
    server.quit()


def dumpSentiments(filename, counter):
    global sentimentlist
    outputstring = outputpath + str(filename) + '_sentiments_' + str(counter) + ".csv"
    sentimentfile = open(outputstring,'w',newline='')
    sentimentfilewriter = csv.writer(sentimentfile)
    sentimentfilewriter.writerow(["search_term", "newspaper_domain", "time_period", "response_id", "url",
                "matchtype", "matchedserch_term", "party", "member",
                "entitytype","text", "sentiment", "relevance", "count", "sentiment_id", "category"])
    for elem in sentimentlist:
        row, mtype, match, entity, unique_id, category= elem
        sentimentfilewriter.writerow([row[0], row[1], row[2], row[3], row[4],
                    mtype, match["searchterm"], match["party"], match["member"],
                    entity["type"], entity["text"], entity["sentiment"]["score"], entity["relevance"], entity["count"], unique_id, category])
    print("Saved Sentiments")
    sentimentfile.close()
    sentimentlist = []
    counterstring = outputpath + str(filename) + "_counter.txt"
    file = open(counterstring,"w")
    file.write(str(counter))
    file.close()


def dumpArticleList(filename, counter):
    global articlelist
    outputstring = outputpath + str(filename) + '_texts_' + str(counter) + ".json"
    h = open(outputstring, 'w')
    json.dump(articlelist, h)
    articlelist = []


def saveResults(result, row):
    if(len(result)>=1):
        mydict = dict(search_term=row[0], newspaper_domain=row[1], time_period=row[2], response_id=row[3], url=row[4],analyzed_text=result["analyzed_text"])
        articlelist.append(mydict)
        entities = result["entities"]
        for entity in entities:
            if "sentiment" not in entity:
                print(row[4], "NoSentiment", entity["type"],entity["text"], sep='\t')
            else:
                if entity["type"] == "Person" or entity["type"] == "Organization":
                    mtype, match = matching.matchEntity(entity["text"], row[0])
                    unique_id = uuid.uuid4()
                    category = 1
                    if mtype == 0:
                        category = 0
                    if mtype > 0:
                        print(row[4],entity["text"],match["searchterm"],entity["type"],str(entity["sentiment"]["score"]), sep='\t')
                    element = (row, mtype, match, entity, unique_id, category)
                    sentimentlist.append(element)
                elif entity["type"] == "Date" \
                        or entity["type"] == "Duration" \
                        or entity["type"] == "IPAddress" \
                        or entity["type"] == "Measure" \
                        or entity["type"] == "Money" \
                        or entity["type"] == "Number" \
                        or entity["type"] == "Ordinal" \
                        or entity["type"] == "Percent" \
                        or entity["type"] == "PhoneNumber" \
                        or entity["type"] == "Time":
                    continue
                else:
                    mtype, match = matching.matchEntity(entity["text"], row[0])
                    unique_id = uuid.uuid4()
                    if mtype == 1 or mtype == 2:
                        category = 1
                    elif mtype == 3:
                        category = 0
                    else:
                        category = 0
                    element = (row, mtype, match, entity, unique_id, category)
                    sentimentlist.append(element)
                    if mtype == 1 or mtype ==2:
                        print(row[4],entity["text"],match["searchterm"],entity["type"],str(entity["sentiment"]["score"]),sep='\t')


for i in filenames:
    filestring = i + ".csv"
    sumfile = open(os.path.join(inputpath, filestring), "rU")
    sumreader = csv.reader(sumfile, delimiter=';')
    row_count = sum(1 for row in sumreader) - 1

    file = open(os.path.join(inputpath, filestring), "rU")
    reader = csv.reader(file, delimiter=';')


    counter = 1

    try:
        counterstring = outputpath + str(i) + "_counter.txt"
        counterfile = open(counterstring, "r")
        lastcounter = int(counterfile.read())
        print(lastcounter)
        counterfile.close()
    except:
        print("No counter saved before")
        lastcounter = 1
        pass

    for row in reader:
        if counter < lastcounter:
            counter += 1
        elif row[1] == "newspaper_domain":
            print("Skipping header")
        else:
            try:
                search_term = row[0]
                newspaper_domain = row[1]
                time_period = row[2]
                response_id = row[3]
                url = row[4]

                result, error, errorcounter = Watson.getsentimentfromUrl(url)
                if not error:
                    saveResults(result, row)

                if errorcounter > 4:
                    print("Saving last results")
                    dumpArticleList(i,counter)
                    dumpSentiments(i,counter)
                    messagestring = "Newspaper: " + i + " - Errortermination at response_id: " + str(response_id) + " and counter: " + str(counter)
                    print(messagestring)
                    sentTerminationMail(messagestring)
                    sys.exit("API-ERROR Termination")

                if counter%100 == 0:
                    dumpSentiments(i, counter)
                    dumpArticleList(i,counter)
                if counter%10 == 0:
                    print("Progress in " + i + ": " + str(counter) + "/" + str(row_count) + "     " + str(round((counter/row_count)*100,2)) + "%")

                counter += 1

            except IndexError as ex:
                print("ERROR: %s in file %s has produced a problem" % (row[3], i))
                pass
    #Finalize
    dumpArticleList(i,counter)
    dumpSentiments(i,counter)
    messagestring = "Newspaper: " + i + " - FINISHED at response_id: " + str(response_id) + " and counter: " + str(counter)
    print(messagestring)
    sentTerminationMail(messagestring)






'''
Watson Entity Types

Check normal:
    Organization
    Person

Check for direct matches:
    EmailAddress
    Facility
    GeographicFeature
    Hashtag
    JobTitle
    Location
    TwitterHandle
    URL

Ignore:
    Date
    Duration
    IPAddress
    Measure
    Money
    Number
    Ordinal
    Percent
    PhoneNumber
    Time
'''
