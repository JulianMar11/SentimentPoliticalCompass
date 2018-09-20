import os
import csv

pathName = os.getcwd()
pathName = pathName + "/Input/"

searchtermfile = open(os.path.join(pathName, "searchterms.csv"), "rU")
searchtermreader = csv.reader(searchtermfile, delimiter=';')

#row_count = sum(1 for row in searchtermreader)
#print(row_count)

d = {"searchterm", "forename", "surname", "party", "member"}
searchpoliticians = []
allpoliticiansdict = []

index = 0
for row in searchtermreader:
    #dict = {"searchterm": st, "forename": v, "surname": n, "party": p, "member": ty}

    st, v, n, p, ty = row

    searchpoliticians.append((st, v, n, p, ty))
    mydict = dict(searchterm= st, forename= v, surname=n, party=p, member=ty)
    allpoliticiansdict.append(mydict)

print("Cached Searchitems: " + str(len(searchpoliticians)))

otherpoliticiansfile = open(os.path.join(pathName, "otherpoliticians.csv"), "rU")
otherpoliticiansreader = csv.reader(otherpoliticiansfile, delimiter=';')
otherpoliticians = []

index = 0
for row in otherpoliticiansreader:
    #dict = {"searchterm": st, "forename": v, "surname": n, "party": p, "member": ty}

    st, v, n, p, ty = row

    otherpoliticians.append((st, v, n, p, ty))
    mydict = dict(searchterm= st, forename= v, surname=n, party=p, member=ty)
    allpoliticiansdict.append(mydict)

print("Cached other Politicians: " + str(len(otherpoliticians)))



def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def matchEntity(text,searchterm):
    matchedsearchterm = ""
    bestlev = 100 #MinimunLevenshtein Distance for a match

    #Fast checks for a direct match from searchterm
    searchmatch = False
    fullmatch = False
    surnamematch = False

    searchtermlo = searchterm.lower()
    text = text.lower()
    searchnachname = searchtermlo.split()[-1]


    #entity text in searchterm  (e.g. is Merkel in Angela Merkel
    #searchterm in entity text  (e.g. is Angela Merkel in Bundeskanzlerin Angela Merkel)
    #Surname of searchterm in entity text  (e.g. is Merkel in A. Merkel)
    if (searchtermlo.find(text) != -1 and len(searchtermlo)-len(text) < 5) or text.find(searchtermlo) != -1:
        searchmatch = True
        fullmatch = True
        matchedsearchterm = searchterm
    elif (text.find(searchnachname) != -1):
        searchmatch = True
        surnamematch = True
        matchedsearchterm = searchterm
        bestlev = levenshtein(searchtermlo, text)
    #No searchmatch, search in politician database (computationally high effort)
    else:
        for pol in searchpoliticians:
            if fullmatch:
                break
            polsearchterm = pol[0]
            polsearchtermlo = polsearchterm.lower()
            surname = pol[2].lower()

            #Check Fullmatches
            if (polsearchtermlo.find(text) != -1 and len(polsearchtermlo)-len(text) < 5) or text.find(polsearchtermlo) != -1:
                fullmatch = True
                matchedsearchterm = polsearchterm

            #Check Matches of Surname
            if not fullmatch and text.find(surname) != -1 and len(surname)>=4:
                newlev = levenshtein(polsearchtermlo, text)
                #print("Lev for Pol: " + polsearchterm + " in " + text + " is: " + str(newlev))
                if bestlev == newlev:
                    surnamematch = False
                    matchedsearchterm = ""
                    #print("no clear match")
                    break
                elif bestlev > newlev:
                    bestlev = newlev
                    surnamematch = True
                    matchedsearchterm = polsearchterm

        #Check results in other politician database
        if not searchmatch and not fullmatch and not surnamematch:
            for pol in otherpoliticians:
                if fullmatch:
                    break
                polsearchterm = pol[0]
                polsearchtermlo = polsearchterm.lower()
                surname = pol[2].lower()

                #Check Fullmatches
                if (polsearchtermlo.find(text) != -1 and len(polsearchtermlo)-len(text) < 5) or text.find(polsearchtermlo) != -1:
                    fullmatch = True
                    matchedsearchterm = polsearchterm

                #Check Matches of Surname
                if not fullmatch and text.find(surname) != -1 and len(surname)>=4:
                    newlev = levenshtein(polsearchtermlo, text)
                    #print("Lev for Pol: " + polsearchterm + " in " + text + " is: " + str(newlev))
                    if bestlev == newlev:
                        surnamematch = False
                        matchedsearchterm = ""
                        #print("no clear match")
                        break
                    elif bestlev > newlev:
                        bestlev = newlev
                        surnamematch = True
                        matchedsearchterm = polsearchterm

    lev = "NaN"
    try:
        if searchmatch and fullmatch:
            matchtype = 1
            match = next(item for item in allpoliticiansdict if item["searchterm"] == matchedsearchterm)
        elif not searchmatch and fullmatch:
            matchtype = 2
            match = next(item for item in allpoliticiansdict if item["searchterm"] == matchedsearchterm)
        elif searchmatch and surnamematch:
            matchtype = 3
            match = next(item for item in allpoliticiansdict if item["searchterm"] == matchedsearchterm)
            lev = bestlev
        elif not searchmatch and surnamematch:
            matchtype = 4
            match = next(item for item in allpoliticiansdict if item["searchterm"] == matchedsearchterm)
            lev = bestlev
        else:
            matchtype = 0
            match = {}
            match["searchterm"] = "NaN"
            match["party"] = "NaN"
            match["member"] = "NaN"
            lev = "NaN"
    except:
        matchtype = 0
        match = {}
        match["searchterm"] = "NaN"
        match["party"] = "NaN"
        match["member"] = "NaN"
        lev = "NaN"
        pass
    return (matchtype, match, lev)
