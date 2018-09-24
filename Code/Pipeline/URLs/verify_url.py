

# TODO
# specific processing not required: can be done with URL request module!!!

# verify for each newspaper specifically if the URL exists
# if it not exists, this can have two indications:
    # 1) the HTTP request returns no response -> done within all_urls
    # 2) the HTTP response is proper, but its content indicates that the website does not exist

from Data_pipe.text import open_URL, decode_to_string

def verify_file(file, domain):
    if domain == "www.zeit.de":
        return zeit(file)
    else:
        return False


def zeit(file):
    """
    Verify if the newspaper exists based on the specific error message of the newspaper

    :return:
    """
    html = decode_to_string(file)
    if "Dokument nicht gefunden" in html:
        return False
    else:
        return True



if __name__ == "__main__":
    print(zeit("https://www.zeit.de/politik/deutschland/2017-01/martin-schulz-rede-spd-kanzlerkandidat-bundestagswahlkampf/seite-2"))  # True
    print(zeit("https://www.zeit.de/politik/deutschland/2017-01/martin-schulz-rede-spd-kanzlerkandidat-bundestagswahlkampf/seite-3"))  # False

