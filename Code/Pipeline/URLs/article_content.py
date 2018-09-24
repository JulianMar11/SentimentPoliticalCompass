
# TODO comment out when running text
from Data_pipe.text import open_URL, soup_from_file

# just for testing
from Data_pipe.text import read_byte_content


def extract_article_string(newspaper, soup):
    """
    Beautiful soup documentation: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find_all

    :param soup:
    :return:
    """
    pass

def zeit(soup):
    text = ""
    # title
    html = soup.find("span", {"class": "article-heading__title"})
    text += html.get_text() + "\n"  # strip away the html tags
    # paragraphs
    html_list = soup.find_all("p", {"class": "paragraph article__item"})  # returns list with html tags
    for html in html_list:
        text += html.get_text() + "\n"  # # strip away the html tags; "\n" marks the end of a paragraph, might have to be parsed out later
    return text


if __name__ == "__main__":
    file, verified = open_URL("https://www.zeit.de/politik/deutschland/2017-01/martin-schulz-rede-spd-kanzlerkandidat-bundestagswahlkampf/seite-2")
    soup = soup_from_file(file)

    # extract_article_string("www.zeit.de", soup)
    print(zeit(soup))
