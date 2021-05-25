import requests
from bs4 import BeautifulSoup
from collections import Counter
from string import punctuation

def wordStor(site):
    # We get the url
    r = requests.get(site)
    soup = BeautifulSoup(r.content, features="lxml")

    # We get the words within paragraphs
    text_p = (''.join(s.findAll(text=True)) for s in soup.findAll('p'))
    c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))

    # We get the words within divs
    text_div = (''.join(s.findAll(text=True)) for s in soup.findAll('div'))
    c_div = Counter((x.rstrip(punctuation).lower() for y in text_div for x in y.split()))

    # We sum the two countesr and get a list with words count from most to less common
    total = c_div + c_p
    list_most_common_words = total.most_common(50)

    return list_most_common_words

def addNextLowNum(full_list, search_value, indx):
    # Full_list is ordered from high occurrences to low,
    # in order to reach on the search to popular first
    if indx != -1:
        # Dispose duplications
        over_all.pop(indx)

    for i, lst in enumerate(full_list):
        # Keep the index of the search_value
        if lst[1] <= search_value[1]:
          # First or in the middle
          full_list.insert(i, search_value)
          return (full_list)
    # At rge end of a list
    full_list.append(search_value)
    return (full_list)

def clnGarbdge(fullList):
    # Decidion: len of 1 char that is not currency
    values_list = [(k,r[0]) for k, r in enumerate(fullList) if len(r[0]) < 2]
    accepted_list = ['$','₪','£','¥',' ₣' ,'₤' ,'₧' ,'€' ,'₹' ,'₩' ,'₴' ,'₯','₮','₰' ,'₲', '₱', '₳', '₵' ,'₭' ,'₫']
    #print(values_list)

    values = len(values_list)
    while values:
        if not values_list[values-1][1] in accepted_list:
            del fullList[values_list[values-1][0]]
        values -=1
    return fullList

if __name__ == '__main__':
    arr = ['http://he.wikipedia.org', 'http://ynet.co.il', 'http://www.talniri.co.il']
    word_tuple = {}
    over_all = []
    # For each url in the list, count all words
    for web_page in arr:
        # For each web page Return a list of tuple that include count of words in the web page
        word_tuple = wordStor(web_page)
        #print("New words list", len(word_tuple), word_tuple)
        # Merge lists
        if not over_all:
            # When the over_all list is empty
            over_all = word_tuple.copy()
            continue

        # handle addition of elements while combine the word occurrences from all sites
        for input_value in word_tuple:
            # Combine the word numerator into one ordered list
            values_list = [r[0] for r in over_all]

            indx = values_list.index(input_value[0]) if input_value[0] in values_list else -1
            search = input_value

            if indx != -1:
                # for exists word -  add occurrences
                tmp = (input_value[0], input_value[1] + over_all[indx][1])
                search = tmp

            addNextLowNum(over_all, search,indx)
        #print("Over all list, each round", len(over_all), over_all)

    clnGarbdge(over_all)
    k=len(over_all)
    # print word by its numerator from lower to higher (reverse)
    # reverse operation is costly then print reverse
    while k:
        print("length",over_all[-1][1], end ="")
        print( ":", over_all[-1][0])
        k-=1
        over_all = over_all[:k]



