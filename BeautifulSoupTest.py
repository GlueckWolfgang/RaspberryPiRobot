# -*- coding: utf-8 -*-
###############################################################################
# Test beautiful soup
# Version:  2016.02.13
#
###############################################################################
import json
import re
import codecs
from bs4 import BeautifulSoup as Soup

def get_ids(html_file, regular_expression):
    ids = dict()
    with codecs.open(html_file, 'r', encoding='utf-8', errors='ignore') as fh:
        soup = Soup(fh, 'html.parser')
        for element in soup.find_all('td', id=re.compile(regular_expression)):
            id = element.get('id')
            if id:
                ids[id] = ""
                if id.endswith("_V"):
                # add Cv
                    id = id.replace("_V", "_Cv")
                    ids[id] = ""
    return ids


ids = get_ids("Robbi/Panel.html", r'["id=M_]|["id=S_]+"')
ouput = json.dumps(ids)
print(ouput)