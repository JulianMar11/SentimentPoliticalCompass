

import os

n_pages = 10  # the first 10 pages are checked whether they exist (but stopping), when e.g. page 3 could not be found


# TODO extend
def all_pages(url, domain):
    if domain == "www.zeit.de":
        return zeit(url)
    else:
        # no other pages listed
        return [url]



# functions for finding all possible pages of an article, specific for the newspaper
# note: pages are tried even if "seite" or something similar is not part of the URL
    # reason: there are pages that have a first page without any indication that further pages exist

def zeit(url):
    """
    All pages except the one given in input url, since ???? WHY?????

    Page numbers as last path name component, i.e. .../seite-2
    seite-1 redirects to page without any seite-... info

    :param url:
    :return:
    """
    head, tail = os.path.split(url)  # tail contains only last component

    pages = []
    if "seite" in tail:
        # change only the last digit (can cause duplicates)
        for i in range(1, n_pages+1):
            mod_tail = tail[:-1]  # everything except the last number
            mod_tail += str(i)
            pages.append(os.path.join(head, mod_tail))
    else:
        # add the "seite" tag first and then try all numbers; starting from 2, since "seite-1" redirects
        # to the page without any "seite" information -> otherwise same page twice, but with different URL -> no
        # duplicate -> bias
        tail = os.path.join(tail, "seite-")
        for i in range(2, n_pages + 1):
            mod_tail = tail + str(i)
            pages.append(os.path.join(head, mod_tail))
    return pages








if __name__ == "__main__":
    print(zeit("https://www.zeit.de/politik/deutschland/2017-01/martin-schulz-rede-spd-kanzlerkandidat-bundestagswahlkampf/seite-2"))
    # print(zeit("https://www.zeit.de/politik/deutschland/2017-01/martin-schulz-rede-spd-kanzlerkandidat-bundestagswahlkampf/"))