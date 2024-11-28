import requests
from bs4 import BeautifulSoup

url = "https://en.prothomalo.com/bangladesh/285oxkxekf"
a = requests.get(url)
soup = BeautifulSoup(a.content, "html5lib")
title = soup.find('h1', class_='IiRps')
print(title.text)









#<span class="tilte-no-link-parent"> 15 ministers, 13 state ministers dropped</span>