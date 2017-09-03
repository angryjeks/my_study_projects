#import urllib
from time import sleep

import requests
from bs4 import BeautifulSoup
from lxml import html

url = "https://api.telegram.org/bot429192506:AAE95HG2J9Lf4K1Leo47iAibxoGrrcyRAPQ/"

flib = 'http://flibusta.is/booksearch'

b_url = 'http://flibusta.is'

Num = 5

"""def get_ul(text):
    t = ''
    val_p = text.find('<ul>')
    val_l = text.find('</ul>')
    for i in range(val_p + 4, val_l):
        t += text[i]
    return t
"""
class Book:
    def __init__(self, name, author, name_u, author_u):
        self.name, self.author, self.name_u, self.author_u  = name, author, name_u, author_u

    def printb(self):
        a = "<a href = \"" + self.name_u + "\">" + self.name + "</a>   -   <a href = \"" + self.author_u + "\">" + self.author + "</a>"
        return a

    def getNameU(self):
        return self.name_u




def get_updates_json(request):
    params = {'timeout':100, 'offset':None}
    response = requests.get(request + 'getUpdates', data = params)
    return response.json()

def send_photo(chat, url1):
    params = {'chat_id' : chat, 'photo' : url1}
    response = requests.post(url + 'sendPhoto', data = params)
    return response


def last_update(data):
    results = data['result']
    return results[-1]

def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id

def send_mess(chat, text):
    params = {'chat_id' : chat, 'text' : text, 'parse_mode' : 'HTML'}
    response = requests.post(url + 'sendMessage', data = params)
    return response

def main():
    update_id = last_update(get_updates_json(url))['update_id']
    ph_ex = True
    while True:
        ph_url = ""
        last_upd = last_update(get_updates_json(url))
        if update_id == last_upd['update_id']:
            chat_id = get_chat_id(last_upd)
            text = last_upd['message']['text']
            payload = {'ask' : text, 'chs' : 'on', 'cha' : 'on', 'chb' : 'on'}
            with requests.session() as s:
                resp = s.get(flib, params = payload)
                tree = html.fromstring(resp.text)
                #xpath = tree.xpath('//div[@id="main"]/ul')
                #ul = xpath[0].xpath('li/a/@href')
                bookshelf = []
                mess = ""
                lis = []
                num = Num
                try:
                    t1 = tree.xpath('//div[@id="main"]/h3[contains(text(), "Найденные книги")]/following-sibling::ul[1]')[0]
                except IndexError:
                    mess += "Книг не найдено."
                    num -= 5
                for i in range(1,num+1):
                    lis.append(str(i))
                for i in lis:
                    try:
                        book = Book("".join(t1.xpath('li['+i+']/a[1]//text()')),
                                    "".join(t1.xpath('li['+i+']/a[2]//text()')),
                                    b_url + t1.xpath('li['+i+']/a[1]/@href')[0],
                                    b_url + t1.xpath('li['+i+']/a[2]/@href')[0])
                    except IndexError:
                        break

                    
                    bookshelf.append(book)

                    resp = s.get(book.getNameU())
                    tree = html.fromstring(resp.text)
                    j = 0
                    path = tree.xpath('//div[@id="main"]//a') 
                    x = path[0].xpath('text()')[0]
                    #print(x)
                    while x[0] != "(":
                        j +=1
                        try:
                            x = path[j].xpath('text()')[0]
                        except IndexError:
                            continue
                        #x = apath
                        xpath = b_url + path[j].xpath('@href')[0]
                        #print(x)
                    if x == "(читать)":
                        x = path[j+1].xpath('text()')[0]
                        xpath = b_url + path[j+1].xpath('@href')[0]
                    mess += "\n" + book.printb() + "\nСкачать в формате <a href=\"" +xpath + "\">" + x + "</a>"
                   
                    if i == '1':
                        try:
                            xp1 = tree.xpath('//h2[contains(text(), "Аннотация")]/following-sibling::p[1]/text()')[0]
                        except IndexError:
                            xp1 = "Аннотации нет."
                        mess += "\n" + "Аннотация:\n" + xp1
                        
                        try:
                            ph_url = b_url + tree.xpath('//img[@alt="Cover image"]/@src')[0]
                        except IndexError:
                            ph_url = ""
                    mess += "\n------------------------"
                    print(i)
            #print(ph_url)
            send_mess(chat_id, mess)
            
            send_photo(chat_id, ph_url)
            update_id +=1
    sleep(1)


if __name__ == '__main__':
    main()
