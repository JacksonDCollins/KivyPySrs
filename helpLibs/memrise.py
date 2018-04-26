#!/usr/bin/env python
COURSE_URL = 'https://www.memrise.com/course/78463/hacking-russian-2/2/'
COURSES_URL = 'https://www.memrise.com{}languages/'.format('/courses/english/')
CARD_COLUMNS = ("col_a", "col_b")

import codecs, sys
import os
import re

from requests_html import HTMLSession
from requests_html import HTML
import asyncio

from datetime import datetime, timedelta

def lazy_property(fn):
    """Decorator that makes a property lazy-evaluated.
    """
    attr_name = '_lazy_' + fn.__name__

    @property
    def _lazy_property(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazy_property


def get_soup(url, session = None):
    if session:
        res = session.get(
            url if url.strip().startswith("http") else "http://www.memrise.com" + url)
        soup = BeautifulSoup(res.text, "lxml")
        return soup
    else:
        soup = BeautifulSoup(url, "lxml")
        return soup

class CourseBrowser(object):
    def __init__(self):
        payload = { "username": "MyPySrs", 
                        "password": "MyPySrs", 
                        "csrfmiddlewaretoken": "<TOKEN>"
                        }
        self.session =  HTMLSession()
        login_url = 'https://www.memrise.com/login/'
        result = self.session.get(login_url)
        tree = result.html #html.fromstring(result.text)
        authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]
        payload['csrfmiddlewaretoken'] = authenticity_token

        self.session.post(login_url, data = payload, headers = dict(referer=login_url)) 

        self.courses_url = COURSES_URL

        self.page = None
        self.getLanguages()

    def selfExit(self):
        self.browser.quit()

    def getLanguages(self):
        self.allLangsHrefs = {}
        soup = self.session.get(self.courses_url)
        el = soup.html.find("ul.categories-list[data-default-category-id = '569']", first = True)
        allLangs = el.find('a')
        for i in allLangs:
            self.allLangsHrefs[i.text] = i.absolute_links.pop()
        
        self.coursesDict = {}

        lis = el.find("ul.{}[data-default-category-id = '{}']>li".format(el.attrs['class'][0], el.attrs['data-default-category-id']))
        for i in lis:
            Topname = i.find('a', first = True).text
            self.coursesDict[Topname] = []
            ul = i.find("ul", first = True)
            lis2 = ul.find("li")
            for i in lis2:
                Midname = i.find('a', first = True).text
                self.coursesDict[Topname].append(Midname)

    def loadCourses(self, lang):
        self.courses_url = self.allLangsHrefs[lang]
        self.req = self.session.get(self.courses_url)
    
    def on_pre_leave(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(t())

        async def t():
            await self.req.html.page.close()

    def loadMore(self):
        url = self.req.url
        loop = asyncio.get_event_loop()

        if not self.page: 
                self.req.html.render(keep_page = True)
                self.page = self.req.html.page

        async def render():
            try: await self.page.click('a.infinite-scroller-trigger')
            except: pass
            await self.page.evaluate('window.scrollTo(0, document.body.scrollHeight);')
            await self.page.waitForSelector('a.infinite-scroller-trigger', visible = True)
            t = await self.page.content()
            return t
        return loop.run_until_complete(render())

    def getHtml(self, url):
        return self.session.get(url)

    def getCourses(self, url = None, page = None):
        if not url:
            soup = HTML(html=page)
        else:
            soup = self.getHtml(url).html

        featured = soup.find('a.featured-course-box', first = True)
        courses = soup.find('div.course-box-wrapper')
        coursesList = [featured]
        for i in courses:
            coursesList.append(i)
        return coursesList

class Course(object):
    def __init__(self, course_url, supLangs):
        self.supLangs = supLangs
        payload = { "username": "MyPySrs", 
                        "password": "MyPySrs", 
                        "csrfmiddlewaretoken": "<TOKEN>"
                        }
        self.session =  HTMLSession()
        login_url = 'https://www.memrise.com/login/'
        result = self.session.get(login_url)
        tree = html.fromstring(result.text)
        authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]
        payload['csrfmiddlewaretoken'] = authenticity_token

        self.session.post(login_url, data = payload, headers = dict(referer=login_url)) 

        match = re.match(r'^(.*)/(\d+)/?$', course_url)
        if match:
            course_url, level = match.groups()
        else:
            level = None

        self.course_url = course_url
        # a sligle level if it was included in the URL
        self.level = level

    @property
    def soup(self):
        return get_soup(self.course_url, self.session)

    @property
    def name(self):
        el = self.soup.find("h1", class_="course-name")
        return el.text if el else self.course_url.split('/')[-1]

    @property
    def lang(self):
        el = self.soup.find("div", class_="course-breadcrumb")
        el = el.find_all('a')
        return el[len(el)-1].text.strip()

    @property
    def levels(self):

        #levels = soup.find(lambda tag: tag.name == "div" and "levels" in tag.attrs.get("class"))
        levels = self.soup.find_all("a", class_="level")

        for l in levels:
            url = l.attrs.get("href")
            if self.level and not url.endswith(self.level + '/'):
                continue  ## skip lelevel not requested

            title = l.find("div", class_="level-title").text.strip()
            yield (url, title)


    def cards(self, *, level_url : str):
        """
        :level_url:   level URL
        """
        def get_text(value):
            if 'image' in value['class']:
                return  '{}-{}'.format('img', value.img['src'])
            elif 'text' in value['class']:
                return value.text
            elif 'audio' in value['class']:
                return '{}-{}'.format('audio', value.a['href'])

        soup = get_soup(level_url, self.session)

        for thing in soup.find_all(lambda tag: tag.has_attr("data-thing-id")):
            try:
                cols = (get_text(thing.find("div", class_=col_name).find("div", class_=("text",'image','audio'))) for col_name in CARD_COLUMNS)
            except:
                continue

            yield cols

    def fix(self):
        linesfromMemrise = self.mylines
        curdate = "{}/{}/{}".format(datetime.now().day,datetime.now().month,datetime.now().year)
        returnlist = []
        #try:
        lenr = len(linesfromMemrise)
        for n,i in enumerate(linesfromMemrise):
            levelcount = 1
            i = i.replace("\n", "")
            i = i.split('\t')
            i[0] = i[0].replace(",", "commaChar")
            i[1] = i[1].replace(",", "commaChar")
            lang = i[4]
            i[4] = '0'
            i.append("0")
            i.append(curdate)
            i.append("none")
            i.append(curdate)
            i.append("0")
            i.append("")
            i.append(i[2])
            i[2] = 'none'
            i.append(i[3])
            #i[2] = download(i[0])
            i[3] = "no"
            i.append("no")
            i.append(self.supLangs[lang])           
            returnlist.append(i)
        #except Exception as e:
        #   print("dasf", e)
        #   pass
                                
                            
        tmplist = []
        levelcount = 0
        lastLevel = None
        for l in returnlist:
            if l[12] == lastLevel:
                pass
                #l[3] = "Level{}".format(levelcount)
                #tmplist.append(",".join(l))
            else:
                lastLevel = l[12]
                levelcount += 1
            l[12] = "Level{}".format(levelcount)
            tmplist.append(",".join(l))
        self.newCourse = tmplist

    def dump_course(self):
        """
        :course_url:   course URL
        """
        mylines = []
        lNum = 1
        valid = False
        if len([(x,y) for x,y in self.levels]) > 0:
            for level_url, title in self.levels:
                for card in self.cards(level_url=level_url):
                    ent ='\t'.join(card).split('\t')
                    if not ent[0] == '' and not ent[1] == '':
                        #print("\t".join([ent[0], ent[1], course.name, 'Level{}'.format(lNum), course.lang]))
                        mylines.append("\t".join([ent[0], ent[1], self.name, 'Level{}'.format(lNum), self.lang]).replace(',','commaChar'))
                        valid = True
                    else: valid = False
                if valid:
                    lNum += 1
        else:
            for card in self.cards(level_url=self.course_url):
                ent ='\t'.join(card).split('\t')
                if not ent[0] == '' and not ent[1] == '':
                    #print(",".join([ent[0], ent[1], course.name, 'Level{}'.format(lNum), course.lang]))
                    mylines.append("\t".join([ent[0], ent[1], self.name, 'Level{}'.format(lNum), self.lang]).replace(',','commaChar'))
                    valid = True
                else: valid = False
            if valid:
                lNum += 1
        self.mylines = mylines

t = CourseBrowser()
