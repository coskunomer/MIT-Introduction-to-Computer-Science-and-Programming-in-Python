# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Ömer Coşkun
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):

    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase
    
    def is_phrase_in(self, text):

        punc_text = "".join([i if i not in list(string.punctuation) else " " for i in text.lower()])

        splited_text = " ".join(punc_text.split()) + " "

        clean_phrase = "".join([i if i not in list(string.punctuation) else " " for i in self.phrase.lower()])

        splited_phrase = " ".join(clean_phrase.split()) + " " 

        if splited_phrase in splited_text:
            check = True
        else:
            check = False
    
        return check

# Problem 3
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        self.phrase = phrase

    def evaluate(self, story):

        return self.is_phrase_in(story.get_title().lower())

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        self.phrase = phrase

    def evaluate(self, story):

        return self.is_phrase_in(story.get_description().lower())


# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
    def __init__(self, EST):
        self.EST = datetime.strptime(EST, "%d %b %Y %H:%M:%S")

    
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

# Problem 6
class BeforeTrigger(TimeTrigger):

    def evaluate(self, story):

        try:

            if story.get_pubdate() < self.EST:

                return True
        
        except:

            self.EST = self.EST.replace(tzinfo = pytz.timezone("EST"))
            
            if story.get_pubdate() < self.EST:
                
                return True

        return False

class AfterTrigger(TimeTrigger):

    def evaluate(self, story):

        try:

            if story.get_pubdate() > self.EST:
                return True
        
        except:

            self.EST = self.EST.replace(tzinfo = pytz.timezone("EST"))
            if story.get_pubdate() > self.EST:
                return True

        return False


# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):

    def __init__(self, T):
        self.T = T

    def evaluate(self, story):
        return not self.T.evaluate(story)

# Problem 8
class AndTrigger(Trigger):

    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def evaluate(self, story):
        if self.arg1.evaluate(story) and self.arg2.evaluate(story):
            return True
        else:
            return False

# Problem 9
class OrTrigger(Trigger):

    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def evaluate(self, story):
        if self.arg1.evaluate(story) or self.arg2.evaluate(story):
            return True
        else:
            return False


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    filtered_list = []
    for i in stories:
        if any([cond.evaluate(i) for cond in triggerlist]) == True:
            filtered_list.append(i)
    stories = filtered_list

    return stories


#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!

    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers
    c_dict = {"TITLE": TitleTrigger, "DESCRIPTION": DescriptionTrigger, "AFTER": AfterTrigger, "BEFORE": BeforeTrigger,
    "AND": AndTrigger, "OR": OrTrigger, "NOT": NotTrigger}
    trigger_list = []
    trigger_dict = dict()
    for i in lines:
        i = "".join(i)
        i = i.split(",")
        if i[0] == "ADD":
            trigger_list.append(trigger_dict[i[1]])
            trigger_list.append(trigger_dict[i[2]])
        elif i[1] == "OR" or i[1] == "AND":
            trigger_dict[i[0]] = c_dict[i[1]](trigger_dict[i[2]], trigger_dict[i[3]])
            trigger_list.append(trigger_dict[i[0]])
        else:
            trigger_dict[i[0]] = c_dict[i[1]](i[2])
            trigger_list.append(trigger_dict[i[0]])
    
    #print("====", trigger_dict, "====")

    return trigger_list


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        #t1 = TitleTrigger("Coronavirus")
        #t2 = DescriptionTrigger("Fahrettin Koca")
        #t3 = DescriptionTrigger("Turkey")
        #t4 = AndTrigger(t2, t3)
        #triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

