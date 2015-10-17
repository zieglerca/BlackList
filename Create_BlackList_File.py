import sys, os, urllib.request
from bs4 import BeautifulSoup  # 'requires pip install'

# Python script to scrape the top 500 adult sites from alexa
# and put it into a text file. The text file will then be used
# as a blacklist for fritzbox
blacklist = ""

# This website contains the bad adult pages!
#   Page 1:     http://www.alexa.com/topsites/category/Top/Adult
#   Page 20:    http://www.alexa.com/topsites/category;19/Top/Adult
alexa_urls = []
alexa_urls.append("http://www.alexa.com/topsites/category/Top/Adult")
for i in range(1,20):
    alexa_urls.append("http://www.alexa.com/topsites/category;" + str(i) + "/Top/Adult")

for alexa_url in alexa_urls:
    response = urllib.request.urlopen(alexa_url)
    soup = BeautifulSoup(response.read(), 'html.parser')

    # Each entry in the list has the following structure:
    # <p class="desc-paragraph"><a href="/siteinfo/smokingsides.com">Smokingsides.com</a></p>
    for link in soup.find_all('a'):
        if link.is_empty_element is not True and \
           'href' in link.attrs.keys()       and \
           type(link.attrs['href']) is str   and \
           link.attrs['href'].startswith("/siteinfo/") is True:
            # replace /siteinfo/ with a space and append it to the complete list
            blacklist += link.attrs['href'].replace("/siteinfo/", " ")

# Then we output the list into a file that can be understood by Fritz.box
file = open("BlackList.txt", "w")
file.write(blacklist)
file.close()