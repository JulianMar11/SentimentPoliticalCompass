

from datetime import datetime
import os
import dateutil
from dateutil import parser

# TODO comment out when running text
from Data_pipe.text import open_URL, soup_from_file


url_database_path = os.path.join("/Users/FabianFalck/Documents/[03]PotiticalCompass_PAPER/SPC/Paper/Code/Data_pipe", "all_urls.xlsx")
url_verified_database_path = os.path.join("/Users/FabianFalck/Documents/[03]PotiticalCompass_PAPER/SPC/Paper/Code/Data_pipe", "all_urls_verified.xlsx")

def range_to_dates(range_string):
    # find position of ":" and split in half
    colon_pos = range_string.find(":")
    start_string = range_string[:colon_pos]
    end_string = range_string[colon_pos+1:]

    # convert into datetime
    start = datetime.strptime(start_string, "%Y%m%d")
    end = datetime.strptime(end_string, "%Y%m%d")
    return start, end

def extract_date(newspaper, soup):
    if newspaper == "www.zeit.de":
        return zeit(soup)


def check_date(date, start, end):
    """
    https://stackoverflow.com/questions/8142364/how-to-compare-two-dates

    :param date:
    :param start:
    :param end:
    :return:
    """
    if date >= start and date <= end:
        return True
    else:
        return False


class GermanParserInfo(dateutil.parser.parserinfo):
    """
    Documentation, in case other things than just the Month have to be changed: https://dateutil.readthedocs.io/en/stable/parser.html
    https://stackoverflow.com/questions/37485174/python-locale-in-dateutil-parser
    """
    MONTHS = [("Jan", "Januar"),
              ("Feb", "Februar"),
              ("Mar", "März"),   # TODO ä issue?
              ("Apr", "April"),
              ("May", "Mai"),
              ("Jun", "Juni"),
              ("Jul", "Juli"),
              ("Aug", "August"),
              ("Sep", "September"),
              ("Oct", "Oktober"),
              ("Nov", "November"),
              ("Dec", "Dezember")]


def verify_article_date():
    search_terms = retrieve_column("A", url_database_path)
    newspaper_domains = retrieve_column("B", url_database_path)
    time_periods = retrieve_column("C", url_database_path)
    response_ids = retrieve_column("D", url_database_path)
    urls = retrieve_column("E", url_database_path)

    # TODO?


def zeit(soup):
    """
    <time itemprop="datePublished" datetime="2017-01-29T18:08:33+01:00" class="metadata__date">29. Januar 2017, 18:08 Uhr</time>

    :param soup:
    :return:
    """
    try:
        # date string could be extracted, i.e. first page of an article
        date_string = soup.find("time", {"class": "metadata__date"}).get_text()  # returns list with html tags
    except:
        # date string could NOT be extracted, i.e. subsequent page of an article
        date_string = "NA"

    # remove everything from and including the comma
    date_string = date_string[:date_string.find(",")]
    return date_string

if __name__ == "__main__":
    file, verified = open_URL("https://www.zeit.de/politik/deutschland/2017-01/martin-schulz-rede-spd-kanzlerkandidat-bundestagswahlkampf/seite-1")
    soup = soup_from_file(file)

    start, end = range_to_dates("20170116:20170218")

    date_string = extract_date("www.zeit.de", soup)  # date time object
    print(date_string)
    date_object = parser.parse(date_string, parserinfo=GermanParserInfo())
    print(date_object)

    print(check_date(date_object, start, end))


    # actual running