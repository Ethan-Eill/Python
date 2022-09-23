import requests
from bs4 import BeautifulSoup

#get website home page and store it in soup
URL = 'https://www.imdb.com/'
r = requests.get(URL)
soup = BeautifulSoup(r.content, 'html5lib')

#print(soup.prettify())

#prints top x amount of movies
def print_top_movies(input):
    print("Top movies...\n")
    counter = 1

    #navigate to href where top 250 movies are located
    rq = requests.get('https://www.imdb.com/chart/top/?ref_=nv_mv_250')
    movies_html = BeautifulSoup(rq.content, 'html5lib')

    #narrow down html code to find where movie titles are
    lister = movies_html.find("tbody", attrs={"class":"lister-list"})
    tr = lister.findAll("tr")

    #loop through and print x amount of movie titles
    for item in tr:
        name = item.find("td", attrs={"class":"titleColumn"})
        movie_name = name.a.text
        print(counter, end=". ")
        print(movie_name)
        counter+=1
        input -= 1
        if input == 0:
            break

#print top box office performers
def print_box_office_movies():
    print("Top box office movies from past week...\n")
    counter = 1

    #get link
    rq = requests.get('https://www.imdb.com/chart/boxoffice/?ref_=nv_ch_cht')
    box_html = BeautifulSoup(rq.content, 'html5lib')

    #navigate to where titles are in the html
    tbody = box_html.find("tbody")
    tr = tbody.findAll("tr")

    #loop through and print the movie title and how much money it total grossed
    for item in tr:
        name = item.find("td", attrs={"class":"titleColumn"})
        movie_name = name.a.text
        print(counter, end=". ")
        print(movie_name, end=" - ")

        gross = item.find("span", attrs={"class":"secondaryInfo"})
        print(gross.text)
        counter+=1


#print movies coming soon
def print_coming_soon():
    print("Movies coming soon...\n")

    #navigate to link
    rq = requests.get('https://www.imdb.com/movies-coming-soon/?ref_=nv_mv_cs')
    cs_html = BeautifulSoup(rq.content, 'html5lib')

    #navigate to information
    list_detail = cs_html.find("div", attrs={"class":"list detail"})
    h4 = list_detail.findAll("h4")

    #loop through and print information, h4 includes the date of release
    #and the movie titles coming out that day
    for item in h4:
        print(item.text)

#print top x amount of shows
def print_top_shows(input):
    print("Top shows...\n")
    counter = 1

    #navigate to href where top 250 shows are located
    rq = requests.get('https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250')
    shows_html = BeautifulSoup(rq.content, 'html5lib')

    #narrow down html code to where show titles are located
    lister = shows_html.find("tbody", attrs={"class":"lister-list"})
    tr = lister.findAll("tr")

    #loop through tr and print x amount of shows
    for item in tr:
        name = item.find("td", attrs={"class":"titleColumn"})
        show_name = name.a.text
        print(counter, end=". ")
        print(show_name)
        counter+=1
        input-=1
        if input == 0:
            break

#user interface
def user_interface():
    print("\n\n")
    print("1.List top movies based off ranking")
    print("2.List top box office movies from past week")
    print("3.List movies coming soon")
    print("4.List top shows based off ranking")
    print("5.Exit program\n\n")
    user_input = input("What would you like to do?\n")
    inp = int(user_input)
    return inp

while True:
    user_in = user_interface()
    #edge cases and exit case
    if user_in < 1 or user_in > 5:
        print("Please enter correct input\n")
    if user_in == 5:
        break
    if user_in == 1:
        num_top_movies = int(input("\nHow many top movies would you like to view?(250 max)\n"))
        print_top_movies(num_top_movies)
    if user_in == 2:
        print_box_office_movies()
    if user_in == 3:
        print_coming_soon()
    if user_in == 4:
        num_top_shows = int(input("\nHow many top shows would you like to view?(250 max)\n"))
        print_top_shows(num_top_shows)
