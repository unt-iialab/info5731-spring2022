# -*- coding: utf-8 -*-
# Created by Utsav on 12/17/2019
import requests
import json

data = {
    "authors": [],
    "coAuthors": [],
    "externalContentTypes": [],
    "pageSize": 10,
    "publicationTypes": [],
    "queryString": "Machine Learning",
    "requireViewablePdf": False,
    "sort": "relevance",
    "venues": [],
    "yearFilter": None
}


# function to traverse the list of authors in a paper


def traverse(x):
    if isinstance(x, list):
        for v in x:
            traverse(v)
    elif isinstance(x, dict):
        if 'name' in x:
            authors.append(x['name'])
        else:
            for v in x.values():
                traverse(v)


# Looping over the pages


for item in range(1, 5):  # increase the range size here to extract more pages
    data['page'] = item
    print(f"{'-' * 36}Extracting Page #{item}{'-' * 36}")
    request = requests.post('https://www.semanticscholar.org/api/1/search', json=data).json()
    # print(request)
    print(request.keys())
    just_results = request['results']
    print(just_results)

    # Iterating and Printing the information of the articles:
    for values in just_results:
        print("\nPaper ID :", values['id'], "\tArticle :", values['title']['text'])
        authors = []
        traverse(values['authors'])
        print("Author(s) :", authors)
        print("Year :", values['year']['text'], "\nAbstract :", values['paperAbstract']['text'],
              "\nTotal number of citations :", values['citationStats']['numCitations'], "\nHighly Influential Papers :",
              values['citationStats']['numKeyCitations'])

        # try:
        #     print("Article :",values['title']['text'],":", "Author(s) :",values['authors'][len(values['authors'])]['name'],"-----","Total number of citations -",values['citationStats']['numCitations'],"-----","Highly Influential Papers -",values['citationStats']['numKeyCitations'])
        # except IndexError:
        #     print(values['title']['text'], ":", "URL Missing")

# Pages info
num_page = request['totalPages']
print(num_page)
