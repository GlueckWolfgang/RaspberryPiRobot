# -*- coding: utf-8 -*-
###############################################################################
# Test beautiful soup
# Version:  2016.02.13
#
###############################################################################
import re
import codecs
from bs4 import BeautifulSoup as Soup


def get_ids(html_file, regular_expression):
    ids = dict()
    with codecs.open(html_file, 'r', encoding='utf-8', errors='ignore') as fh:
        soup = Soup(fh, 'html.parser')
        for element in soup.find_all('td', id=re.compile(regular_expression)):
            idi = element.get('id')
            if idi:
                ids[idi] = "?"
                if idi.endswith("_V"):
                    # add Cv
                    idi = idi.replace("_V", "_Cv")
                    ids[idi] = "?"
    return ids

# create dictionary

template_M = (get_ids("Robbi/Panel.html", r"M_+"))

print(template_M)

for key in template_M:
    mvid = key.split("_")
    print (key)
    print(mvid[0], mvid[1], mvid[2])
    No = int(mvid[1])
    print(str(No))





