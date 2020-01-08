import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from jops.models import Headline
requests.packages.urllib3.disable_warnings()

def news_list(request):
	headlines = Headline.objects.all()[::-1]
	context = {
		'object_list': headlines,
	}
	return render(request, "jops/home.html", context)

def scrape(request):
      session = requests.Session()
      session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
      url = "https://www.upwork.com/search/jobs/?q=django"
      content = session.get(url, verify=False).content
      soup = BSoup(content, "html.parser")
      jops = soup.find_all('div', {"class":"jop-title"})
      for artcile in jops:
        main = artcile.find_all('a')[0]
        link = main['href']
        image_src = str(main.find('img')['srcset']).split(" ")[-4]
        title = main['title']
        jop_headline = Headline()
        jop_headline.title = title
        jop_headline.url = link
        jop_headline.image = image_src
        jop_headline.save()
      return redirect("../")
