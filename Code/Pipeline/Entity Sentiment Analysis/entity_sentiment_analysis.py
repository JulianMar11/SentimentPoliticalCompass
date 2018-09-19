#print(downloader.supported_languages_table("sentiment2", 3))

## download polyglot modules

from polyglot.downloader import downloader
downloader.download("sentiment2.de")
downloader.download("ner2.de")
downloader.download("embeddings2.de")
print("\n")
#downloader.list(show_packages=False)

from polyglot.text import Text
import re
import statistics
import sys






## extraction functions___________________

def read_file(path, file):
    """
    reading .txt file and return its content as string
    :param path: path to file
    :param file: file (.txt)
    :return: file_content as string
    """
    file_name = str(path) + str(file)

    with open(file_name + '.txt', 'r') as myfile:
        file_content = myfile.read()

    return file_content




def pack_keywords(keywords_raw):
    """
    keyword preprocessing
    :param keywords_raw: keywords as string
    :return: list of keywords
    """
    keywords = list()

    ## split lines and words and make 2d array
    for line in keywords_raw.splitlines():
        k_len = line.split(",")
        k_synonyms = list()

        for k in range(0, len(k_len)):
            keyword = k_len[k].strip(' ')
            k_synonyms.append(keyword)

        keywords.append(k_synonyms)

    return keywords




def pack_article(article_raw):
    """
    article preprocessing, splitting paragraphs
    :param article_raw: article as string
    :return: list of paragraphs
    """

    article = list()
    article_split = re.split(r'(?<=>)(.+?)(?=<)', article_raw)

    ## parse articles (no tags)
    for p in range(1, len(article_split), 2):
        article.append(article_split[p])

    return article






def analyze(article, keywords):
    """
    search if article contains any keywords and if so, calculate entity sentiment
    :param article: list of paragraphs
    :param keywords: list of keywords
    :return: unorganized list of dictionaries
    """

    ## [n_paragraph][keywords][sentiment]
    analysis_result = list()

    ## parse paragraphs
    for p in range(0,len(article)):

        keyword_sentiment = dict()

        analyze_paragraph = Text(article[p])
        paragraph_entities = analyze_paragraph.entities

        for e in range(0, len(paragraph_entities)):

            ## remove [' ']
            entity = re.sub('\[\'', '', str(paragraph_entities[e]))
            entity = re.sub('\'\]', '', entity)

            ## check sentiment within whole paragraph
            for group in range(0, len(keywords)):

                if (entity in keywords[group]):

                    representative_keyword = keywords[group][0]
                    ## calculate sentiment and append to dict

                    ## already exists in dict
                    if representative_keyword in keyword_sentiment:

                        keyword_sentiment[representative_keyword].append(get_sentiment(paragraph_entities[e]))

                    ## new keyword to list
                    else:

                        sentiments = list()
                        sentiments.append(get_sentiment(paragraph_entities[e]))
                        keyword_sentiment[representative_keyword] = sentiments

        analysis_result.insert(p, keyword_sentiment)


    return analysis_result





## sentiment analysis functions___________________

def get_sentiment(entity):
    """
    performs entity sentiment analysis
    :param entity: entity to perform entity sentiment analysis on including embedding paragraph
    :return: sentiment value as integer
    """

    positive_sentiment  = entity.positive_sentiment
    negative_sentiment  = entity.negative_sentiment

    ## cut value if larger than 1
    if (positive_sentiment > 1):
        positive_sentiment = 1
    if (negative_sentiment > 1):
        negative_sentiment = 1

    sentiment = (positive_sentiment - negative_sentiment)

    return sentiment






def weight_paragraph(analysis_results, weighting_metric):
    """
    weight metric within paragraphs
    :param analysis_results: list of dicts
    :param weighting_metric: String
    :return: weighted analysis_results dictionary
    """

    for p in range(0,len(analysis_results)):

        ## weight within paragraph
        paragraph = analysis_results[p]
        keys = list(paragraph.keys())

        for k in range(0, len(keys)):

            if len(paragraph[keys[k]]) > 1:

                if (weighting_metric == "average"):

                    ## mean of paragraph
                    sentiment_mean = statistics.mean(paragraph[keys[k]])

                    ## change value in analysis results
                    analysis_results[p][keys[k]] = sentiment_mean
                else:

                    sys.exit("select appropriate weighting metric within paragraph")

            else:

                ## strip off list
                analysis_results[p][keys[k]] = analysis_results[p][keys[k]][0]

    return analysis_results





def weight_article(weight_paragraph_result, weighting_metric):
    """
    weight metric between paragraphs
    :param weight_paragraph_result: list of dicts
    :param weighting_metric: String
    :return: weighted weight_paragraph_result (final)
    """

    article_dict = dict()
    weight_article_result = dict()

    weight = len(weight_paragraph_result)

    for p in range(0,len(weight_paragraph_result)):

        paragraph = weight_paragraph_result[p]
        keys = list(paragraph.keys())

        for k in range(0, len(keys)):


            ## weight within paragraph
            if (weighting_metric == "linear"):

                if (keys[k] not in article_dict.keys()):

                    sentiment = paragraph[keys[k]]
                    weighted_sentiment = sentiment * ((weight - p) / weight)
                    #weighted_sentiment = sentiment * (weight - p)

                    sentiments = list()
                    sentiments.append(weighted_sentiment)

                    article_dict[keys[k]] = sentiments

                else:

                    sentiment = paragraph[keys[k]]
                    weighted_sentiment = sentiment * ((weight - p) / weight)
                    #weighted_sentiment = sentiment * (weight - p)
                    article_dict[keys[k]].append(weighted_sentiment)



            elif (weighting_metric == "headline"):

                if (keys[k] not in article_dict.keys()):

                    sentiment = paragraph[keys[k]]
                    weighted_sentiment = 0

                    if (p < 2):

                        weighted_sentiment = sentiment

                    else:

                        weighted_sentiment = sentiment * ((weight - 0.7) / weight)

                    sentiments = list()
                    sentiments.append(weighted_sentiment)

                    article_dict[keys[k]] = sentiments

                else:

                    sentiment = paragraph[keys[k]]
                    weighted_sentiment = 0

                    if (p < 2):

                        weighted_sentiment = sentiment

                    else:

                        weighted_sentiment = sentiment * ((weight - 0.7) / weight)

                    article_dict[keys[k]].append(weighted_sentiment)




            elif (weighting_metric == "uniform"):

                if (keys[k] not in article_dict.keys()):

                    sentiment = paragraph[keys[k]]
                    weighted_sentiment = sentiment


                    sentiments = list()
                    sentiments.append(weighted_sentiment)

                    article_dict[keys[k]] = sentiments

                else:

                    sentiment = paragraph[keys[k]]
                    weighted_sentiment = sentiment
                    article_dict[keys[k]].append(weighted_sentiment)


            else:

                sys.exit("select appropriate weighting metric within article")


    keywords = list(article_dict.keys())

    for k in range(0, len(keywords)):

        ## change value in analysis results
        sentiment = statistics.mean(article_dict[keywords[k]])
        weight_article_result[keywords[k]] = sentiment

    return weight_article_result






def total_sentiment(weight_article_result):
    """
    calculates sentiment of all keywords
    :param weight_article_result: list of dicts
    :return: integer value of total sentiment
    """
    keys = list(weight_article_result.keys())
    total_sentiment = 0

    for k in keys:

        total_sentiment = total_sentiment + weight_article_result[k]

        if len(keys) > 0:
            total_sentiment = round((total_sentiment/len(keys)),2)

        else:
            total_sentiment = 0

    return total_sentiment





## Pipeline___________________________

articles_paths = "/Users/macbookpro/compass/articles/"
keywords_path = "/Users/macbookpro/compass/keywords/"

article_file_a = [0,1,2]
keyword_file_k = ["SPD", "CDU"]

## average
weighting_metric_paragraph = "average"
## uniform, linear, headline
weighting_metric_article = "uniform"


for a in range(0, len(article_file_a)):
    for k in range(0, len(keyword_file_k)):

        ## articles
        article_raw = read_file(articles_paths, article_file_a[a])
        article = pack_article(article_raw)

        ##keywords
        keywords_raw = read_file(keywords_path, keyword_file_k[k])
        keywords = pack_keywords(keywords_raw)

        ## analyze
        analysis_results = analyze(article,keywords)


        ## apply weighting
        weight_paragraph_result = weight_paragraph (analysis_results, weighting_metric_paragraph)
        weight_article_result = weight_article(weight_paragraph_result, weighting_metric_article)

        ## get total sentiment
        keyword_article_sentiment = total_sentiment(weight_article_result)

        print(weight_article_result, "\n-- article ", article_file_a[a], " sentiment towards ", keyword_file_k[k], " is ", keyword_article_sentiment, "\n\n")