import urllib.request
from bs4 import BeautifulSoup

base_url = 'https://ru.wikinews.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%93%D0%BE%D1%80%D0%BE%D0%B4%D0%B0_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83'

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def check(html, word):
    data = BeautifulSoup(html, 'html.parser')

    for group in data.find_all('div', class_='mw-category-group'):
        letter = group.find('h3')
        if letter.text == word[0].upper():
            for city in group.find_all('li'):
                city = city.find('a')
                if city:
                    city_text = city.text

                    if city_text:

#разбиваю на неск частей (иногда вместе с названием города возвращается название страны в скобках)
                        city_ = city_text.split(" (") 
                        #перевожу в нижний регистр для сравнения со словом, которое написал юзер
                        city_name = city_[0].lower() 
                        print("search " + city_name) #это чисто для проверки вывод в консоль
                        
                        if city_name == word:
                            return True
                        else:
                            city = city.find_next_sibling('a')
                else:
                    return False #если не находит такой город, который назвал пользователь
                    
  
    nextpage = ''
    for page in data.find('div', class_='mw-category-generated').find_all('a'):
    	if page.text == "Следующая страница":
            nextpage = page.get('href')
            break
         
    print(nextpage)
    if nextpage:
        return check(get_html('https://ru.wikinews.org' + nextpage), word)


def check_this_city(word):
	return check(get_html(base_url), word)