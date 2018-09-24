

# Google API key: AIzaSyClIF3lP2CjqVTBTTe8TBrgxe1mrctWpXM

# from googleapiclient.discovery import build
# import pprint
#
# my_api_key = "AIzaSyClIF3lP2CjqVTBTTe8TBrgxe1mrctWpXMy"
# my_cse_id = "007090476945672340566:iqdhroqw_x0"
#
# def google_search(search_term, api_key, cse_id, **kwargs):
#     service = build("customsearch", "v1", developerKey=api_key)
#     res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
#     return res['items']

user = 'Fabian'

import sys
sys.path.append("../")

import json, os
from googleapiclient.discovery import build
import uuid
from openpyxl import load_workbook

from Data_pipe.timePeriods import monthly, in_days

from Data_pipe.databases import retrieve_newspaper_domains, retrieve_entities

from Data_pipe.timePeriods import observation_period_start, observation_period_end, next_period

# Google Cloud API key (to use all APIs)
# Fabian key


# list of domains to search at
domain_list = retrieve_newspaper_domains()

# list of entities to search for (entities = search terms)
entity_list, importance_list = retrieve_entities(only_search_terms=False)

# list of time periods to crawl, depending on the persons priority/importance
search_importance_to_initial_range_days = {
    1: 5,    # people like Angela Merkel
    2: 30,  # important people
    3: 30  # all others -> whole time
}

# dictionary mapping from the domain to search at to
# TODO extend

# CSE IDs of the custom search engines

if user == 'Fabian':
    api_key = "AIzaSyClIF3lP2CjqVTBTTe8TBrgxe1mrctWpXM"

    # Fabian
    domain_to_cse_id = {
        "www.zeit.de": "iqdhroqw_x0",
        "www.tagesschau.de": "cx7q5tggwwu",
        "www.bild.de": "rgxhwfc2lts",
        "www.spiegel.de": "2icqjr3ebpa",
        "www.focus.de": "kxc6jclk8_8",
        "www.faz.net": "tyacm1xn6ja",
        "www.taz.de": "gumsrf4p5fs",
        "www.der-postillon.com": "quxqlapm4zc",
        "www.sueddeutsche.de": "o582yxhd7em",
        "www.unsere-zeit.de": "juqxvmcz44o",
        "www.vorwaerts.de": "eltkopvm0eu",
        "www.bayernkurier.de": "r8opf1wyso8",
        "www.deutsche-stimme.de": "18fgcmm2eao",
        "www.national-zeitung.de": "dp90y7uxdqe",
        "www.welt.de": "dp90y7uxdqe",
        "www.handelsblatt.de": "j8lnnxfjpyo",
        "www.neues-deutschland.de": "e5hameewaz8",
        "www.jungefreiheit.de": "lljy7pt9wqc",
        "www.tagesspiegel.de": "iyr_ttevnoy",
        "www.fr.de": "vqrtnfxq8ca",
        "www.jungewelt.de": "yhnac_lvyoc",
        "www.stern.de": "snwg1hxwj4y",
        "www.n-tv.de": "hn5e01gvvri",
        "www.huffingtonpost.de": "huqvycurusk",
        "www.fdplus.de": "jokhhhtinxg",
        "www.gruene.de": "cqlhpxr8dla",
        "www.union-magazin.de": "47kwmmjdkt0",
        "www.afdkompakt.de": "ujlabgetaku",
    }
    # add the creator string
    for key, value in domain_to_cse_id.items():
        domain_to_cse_id[key] = "007090476945672340566:" + value

elif user == 'Julian':
    api_key = "AIzaSyB2RT19RBcMuV5AeiQwYuquZMZbcmzjcAs"
    # Julian
    domain_to_cse_id = {
        "www.zeit.de": "ue6fdjruvbk",
        "www.tagesschau.de": "ukttl6ms9gy",
        "www.bild.de": "0nmee3prt-8",
        "www.spiegel.de": "jeav5fnyqsw",
        "www.focus.de": "5vcwtwpagry",
        "www.faz.net": "ztkci03vhoe",
        "www.taz.de": "ktx70hzpmwa",
        "www.der-postillon.com": "lhyl3bcoava",
        "www.sueddeutsche.de": "tv5sksfytwm",
        "www.unsere-zeit.de": "8jtgzyvo85y",
        "www.vorwaerts.de": "m4llscjyzb0",
        "www.bayernkurier.de": "vg4blp7hlzo",
        "www.deutsche-stimme.de": "roay5r0yxro",
        "www.national-zeitung.de": "pgmq-vx7j5y",
        "www.welt.de": "tbujugvzxao",
        "www.handelsblatt.de": "vcgffadxgea",
        "www.neues-deutschland.de": "wynpfwqgun4",
        "www.jungefreiheit.de": "k_zfkgtku-a",
        "www.tagesspiegel.de": "mnpqyqwzl1g",
        "www.fr.de": "wa_penivrnm",
        "www.jungewelt.de": "_3bjkpnpl-o",
        "www.stern.de": "ysyujqxm_3y",
        "www.n-tv.de": "c9xrltdozw8",
        "www.huffingtonpost.de": "yojyga4shtm",
        "www.fdplus.de": "3mnxtuteegm",
        "www.gruene.de": "_jfhnsnfruk",
        "www.union-magazin.de": "9-dug7wlunw",
        "www.afdkompakt.de": "ja-zu_eu4i0",
    }

    # add the creator string
    for key, value in domain_to_cse_id.items():
        domain_to_cse_id[key] = "000733123785874779446:" + value

elif user == 'Martina':
    api_key = "AIzaSyD9lE0ggN-assLQnn27ZRp0hfY90HSSU5g"
    # Martina
    domain_to_cse_id = {
        "www.zeit.de": "er2-vnvfkji",
        "www.tagesschau.de": "pv7gt8aj8qu",
        "www.bild.de": "b_fddnuzqyi",
        "www.spiegel.de": "w2pp6iwdsbe",
        "www.focus.de": "tawp1sklxyu",
        "www.faz.net": "pyxcfawqa30",
        "www.taz.de": "k7zeqwyl8hi",
        "www.der-postillon.com": "hobicgtrpi4",
        "www.sueddeutsche.de": "knpx7ngsyaq",
        "www.unsere-zeit.de": "mt2vj71-yba",
        "www.vorwaerts.de": "ba8tllyhpjm",
        "www.bayernkurier.de": "vcrmqjimmdm",
        "www.deutsche-stimme.de": "neltx1xbpty",
        "www.national-zeitung.de": "m1kkxlikiry",
        "www.welt.de": "t8cthjet2uc",
        "www.handelsblatt.de": "qr3f6nwwjii",
        "www.neues-deutschland.de": "cpj9r44gmuw",
        "www.jungefreiheit.de": "batd5w0s90w",
        "www.tagesspiegel.de": "j44f8yd6z_0",
        "www.fr.de": "zqiexd1ztcw",
        "www.jungewelt.de": "ry4pcokdvby",
        "www.stern.de": "cbedeardune",
        "www.n-tv.de": "stp7ijtszoc",
        "www.huffingtonpost.de": "vcvy6sbj2ki",
        "www.fdplus.de": "cqm81kavtrc",
        "www.gruene.de": "gyx1cljhh74",
        "www.union-magazin.de": "4onjw2kgbwi",
        "www.afdkompakt.de": "oqvl0-udsj8",
    }

    # add the creator string
    for key, value in domain_to_cse_id.items():
        domain_to_cse_id[key] = "010446447295514081672:" + value

elif user == 'Niklas':
    api_key = 'AIzaSyBxwZlozilQ8o9T6cXZloAJ0WkTdqitMLI'

    domain_to_cse_id = {
        "www.zeit.de": "vti3me6udiq",
        "www.tagesschau.de": "34q6mfsutq4",
        "www.bild.de": "jqr727srya4",
        "www.spiegel.de": "bl_qyd79zxw",
        "www.focus.de": "gmgftobbqlw",
        "www.faz.net": "1womnzgbers",
        "www.taz.de": "leie9vrh3mu",
        "www.der-postillon.com": "1i7bwxd5gas",
        "www.sueddeutsche.de": "xpglz4rppyq",
        "www.unsere-zeit.de": "m7odhqr7x_g",
        "www.vorwaerts.de": "mz3ekzhq6wy",
        "www.bayernkurier.de": "fh-eq8uxte8",
        "www.deutsche-stimme.de": "8rqwg-uwcyk",
        "www.national-zeitung.de": "4sjpmvjb3ng",
        "www.welt.de": "v-svzixr768",
        "www.handelsblatt.de": "e-voqlmeirg",
        "www.neues-deutschland.de": "-tbh2fssrbs",
        "www.jungefreiheit.de": "glgkic-soos",
        "www.tagesspiegel.de": "bxlwnh959lw",
        "www.fr.de": "veagcbwhi9e",
        "www.jungewelt.de": "jb0xqgaxqse",
        "www.stern.de": "s9hsbm9z3jc",
        "www.n-tv.de": "zo5mo51ti9g",
        "www.huffingtonpost.de": "w8063jgblka",
        "www.fdplus.de": "gpl_caygkau",
        "www.gruene.de": "vnpfdpjkbbw",
        "www.union-magazin.de": "apvzwk5ur6y",
        "www.afdkompakt.de": "krkzgjchqcg",
    }

    # add the creator string
    for key, value in domain_to_cse_id.items():
        domain_to_cse_id[key] = "006130893112909837041:" + value




json_dump_path = "/Users/FabianFalck/Documents/[03]PotiticalCompass_PAPER/Data/json_dump"
# "/Users/FabianFalck/Documents/[03]PotiticalCompass_PAPER/SPC/Paper/Code/Data_pipe/json_dump"
url_database_path = "/Users/FabianFalck/Documents/[03]PotiticalCompass_PAPER/Data/urls.xlsx"
# "/Users/FabianFalck/Documents/[03]PotiticalCompass_PAPER/SPC/Paper/Code/Data_pipe/urls.xlsx"


def get_service():
    """
    Create a Google custom search service object with API version 1

    :return: service object
    """

    service = build("customsearch", "v1",
            developerKey=api_key)
    return service


def custom_search(search_term, newspaper_domain, time_period, page_limit=10):
    """
    Perform a search query using the Google custom search engine API

    General documentation on Google Cloud: https://developers.google.com/api-client-library/python/start/get_started
    Custom search explorer (good for trying stuff out manually): https://developers.google.com/apis-explorer/#p/customsearch/v1/search.cse.list
    Custom search documentation: https://developers.google.com/custom-search/json-api/v1/reference/cse/list
    Custom search with python: https://stackoverflow.com/questions/37083058/programmatically-searching-google-in-python-using-custom-search

    :param search_term: query string to search for
    :param newspaper_domain: newspaper domain (passed as string) to search at. Each newspaper domain has its own custom search engine.
    :param time_period: Range of dates in the format "yyyymmdd:yyyymmdd" from which the query results are retrieved. The dates are estimated by the Google search engine and therefore not guaranteed to be correct.
    :param page_limit: The page_limit most relevant pages are retrieved for one search. A maximum of 10 pages can be retrieved -> must choose time period small enough
    :return: JSON object of the search response
    """

    service = get_service()
    response = []

    # for nPage in range(0, page_limit):
    # print("Reading page number:",nPage+1)

    # list() function returns HTTP request object
    # only .execute() calls the API
    # documentation on dateRestrict: https://developers.google.com/custom-search/json-api/v1/reference/cse/list
        # -> only allows to search in a time period until today
    # documentation on sort: https://developers.google.com/custom-search/docs/structured_data#page_dates
        #  -> Return results from January 1 to February 1 of 2010 (inclusive)
        # https://www.google.com/cse?cx=12345:example&q=oil+spill&sort=date:r:20100101:20100201
        # page date is only an estimate, based on meta tags etc. -> must be verified later
    response.append(service.cse().list(
        q = search_term, # Search term
        cx = domain_to_cse_id[newspaper_domain], # custom search engine ID
        lr = 'lang_de', # German language
        num = page_limit,  # Number of search results to return (maximum: 10)
        sort = "date:r:" + time_period # "date:r:20180520:20180526"  ;  sort = 'date:r:yyyymmdd:yyyymmdd'
    ).execute())
    return response


def extract_urls(response):
    """
    Extract the URLs from the response object

    # structure of response object
    # response[0]  TODO does what?
    # items[]: list: The current set of custom search results. -> page_limit is upper bound of len(items)
    # every item has a link attribute that can be retrieved

    :param response: the resonse object, as executed by custom_search(...)
    :return: list of URLs that are found in the response object
    """

    # for testing
    # print(len(response[0].get("items")))
    # print(response[0].get("items")[0].get("link"))

    if response[0].get("items") is not None:
        # items list contains any items
        url_list = [item.get("link") for item in response[0].get("items")]
    else:
        url_list = []
    return url_list



def store_info(search_term, newspaper_domain, time_period, url_list):
    """
    Writes one line for each tuple (search_term, newspaper_domain, time_period, unique_id, url) into a .xlsx worksheet
    Furthermore, dumps the json response objects into a folder with a unique name

    openpyxl documentation: https://openpyxl.readthedocs.io/en/stable/usage.html

    :param search_term:
    :param newspaper_domain:
    :param time_period:
    :param url_list:
    :return:
    """
    # gernerate a unique identifier
    # documentation: https://docs.python.org/2/library/uuid.html#uuid.uuid4
    unique_id = str(uuid.uuid4())  # str(uuid.uuid4()) generates a unique name

    # store every tuple, as explained above, into one row
    wb = load_workbook(filename=url_database_path)
    sheet = wb['Sheet1']

    for url in url_list:
        row = (search_term, newspaper_domain, time_period, unique_id, url)  # one row per url
        sheet.append(row)
    wb.save(url_database_path)

    # dump the reponse json objects
    with open(os.path.join(json_dump_path, 'id_' + unique_id + '.json'), 'w') as outfile:
        json.dump(response, outfile)

    # close the workbook so that it can be opened after
    wb.close()


def dyn_adjust_time_period(n_urls_received, range_days):
    """
    Dynamically adjusts the time period in which we crawl URLs.

    The protocol is like this:
    If the number of URLs is
     - in [0, 1]: * 2
     - in [2, 3]: * 1.5
     - in [4]: do nothing
     - in range(5, 7): / 1.5
     - in range(7, 11): / 2
    The minimum range is 2 days.
    The maximum range is 60 days.

    :param n_urls_received:
    :param range_days:
    :return:
    """
    if n_urls_received in [0, 1]:
        range_days = int(range_days * 2)
    elif n_urls_received in [2, 3]:
        range_days = int(range_days * 1.5)
    elif n_urls_received in [4]:
        pass
    elif n_urls_received in range(5, 7):
        range_days = int(range_days / 1.5)
    elif n_urls_received in range(7, 11):
        range_days = int(range_days / 2)
    range_days = max(2, range_days)
    range_days = min(180, range_days)

    return range_days


if __name__ == "__main__":
    # search_urls("Angela Merkel", "http://www.zeit.de", "März")

    # one example - August
    # time_periods = ['20170101:20170230']# in_days(10)
    # entity = 'Barbara Hendricks'# 'Alois Karl'
    # domain = 'www.tagesschau.de'
    # time_period = time_periods[0]
    # response = custom_search(entity, domain, time_period)
    # url_list = extract_urls(response)
    # print("URLs received for one search (10 is max): ", len(url_list))
    # store_info(entity, domain, time_period, url_list)

    # results = google_search(
    #     'Angela Merkel', my_api_key, my_cse_id, num=10)
    # for result in results:
    #     print.print(result)

    # toy example
    # print(time_periods[0])


    # toy example
    # response = custom_search("Angela Merkel", "www.zeit.de", time_periods[1], 10)
    # url_list = extract_urls(response)
    # store_info("Angela Merkel", "www.zeit.de", time_periods[1], url_list)


    # sheet_ranges = wb['Sheet1']
    # print(sheet_ranges['A1'].value)

    # searching for URLs of articles
    # print("searches to perform: ", len(domain_list[0:3]) * len(entity_list) * len(time_periods))

    # indices done:
    # 0: 4/8/2018

    # 4: 5/8/2018 -> Martina
    # 6: 6/8/2018 -> Martina

    # 7, 8-11: 6,7/8/2018 -> Niklas

    # print(domain_list[6:7])


    full_entity_list = entity_list
    full_importance_list = importance_list

    domain_list = ['www.unsere-zeit.de', 'www.vorwaerts.de', 'www.bayernkurier.de', 'www.deutsche-stimme.de', 'www.fdplus.de', 'www.gruene.de',
                   'www.national-zeitung.de', 'www.neues-deutschland.de', 'www.union-magazin.de', 'www.afdkompakt.de']



    domain_count = 0

    for d, domain in enumerate(domain_list[9:]):  # only the first newspaper for now
        print("--------------------------------------------------------")
        print("NEW NEWSPAPER: ", domain)
        count = 0

        entity_list = full_entity_list
        importance_list = full_importance_list


        if d == 0:
            # horst_index = full_entity_list.index("")
            spd_index = full_entity_list.index("Maria Michalk")
            entity_list = full_entity_list[spd_index:]
            importance_list = importance_list[spd_index:]



        for entity, importance in zip(entity_list, importance_list):
            # time_periods = search_importance_to_time_periods[importance]
            # get the initial range in days for that entity
            range_days = search_importance_to_initial_range_days[importance]

            # get the intiial start_date
            start_date = observation_period_start

            while start_date < observation_period_end:
                time_period, start_date = next_period(start_date, range_days)
                response = custom_search(entity, domain, time_period, 10)
                url_list = extract_urls(response)
                print("Searched for: (" + entity + ", " + domain + ", " + time_period + ") in # days range: " + str(range_days) + ", urls found: " + str(len(url_list)) + ", # response: " + str(count))
                store_info(entity, domain, time_period, url_list)

                # dynamically adjust the time period to crawl in
                n_urls_received = len(url_list)
                range_days = dyn_adjust_time_period(n_urls_received, range_days)

                # increment counter
                count += 1

                # idea: use first two runs for calibration

        print("--------------------------------------------------------")
        print("NEWSPAPER FULLY DONE!")

        domain_count += 1
    #

