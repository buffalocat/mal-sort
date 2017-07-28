#!/usr/bin/env python
### Let's make a GUI

import kivy
#this makes the choices be less boring
from random import (random, shuffle)
#this makes paths more convenient/safer, hopefully
import os.path
#internal things will be in main, user things in parent
MAINDIR = os.path.dirname(os.path.abspath(__file__))
PARENTDIR = os.path.dirname(MAINDIR)
#this is for getting anime pictures
from urllib import (urlopen, urlretrieve)
from time import sleep
#this is for converting xml to csv
import re

#Holds relevant data from  an anime
#name is actually "title (kind)"
#idnum is a string
class Anime:
    def __init__(self, idnum, name, score):
        self.idnum = idnum
        self.name = name
        self.score = score
        
#kivy

from kivy.app import App

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

from kivy.properties import StringProperty

class ParentScreen(BoxLayout):
    
    def __init__(self, app, **kwargs):
        super(ParentScreen, self).__init__(**kwargs)
        #create necessary screens
        self.app = app
        self.filescreen = FileScreen()
        self.choicescreen = ChoiceScreen()
        #begin on the file screen
        self.add_widget(self.filescreen)

    def loadinfo(self):
        success = True
        try:
            ##data that the ParentScreen keeps track of
            #dictionary of all anime in list
            #(key, value) = (String idnum, Anime anime)
            self.getpics = True
            self.animedict = readcsv(self.getpics)
            #ordered list of sorted anime (treat as BST)
            self.sortedanime = list(filter(lambda x: x in self.animedict.keys(), readsorted()))
            #list of idnums of anime which are yet to be sorted
            #order irrelevant, can be shuffled after creation
            self.unsortedanime = list(filter(lambda x: x not in self.sortedanime, self.animedict.keys()))
        except:
            success = False
            close = Button(text='Ok')
            popup = Popup(title="Something went wrong! Try reimporting .xml", content=close, size_hint=(None, None), size=(400, 300))
            close.bind(on_press=popup.dismiss)
            popup.open()
        if success:
            self.beginchoice()

    def beginchoice(self):
        self.clear_widgets()
        if self.score_threshold < 0:
            self.score_threshold = 0
        if self.rounds <= 0:
            self.rounds = 1
        shuffle(self.unsortedanime)
        self.choicescreen.begin(self.animedict,
                                self.sortedanime,
                                self.unsortedanime,
                                self.rounds,
                                self.score_threshold,
                                self)
        self.add_widget(self.choicescreen)
        
    def endchoice(self):
        writesorted(self.sortedanime)
        writeresults(self.sortedanime, self.animedict)
        close = Button(text='Ok')
        popup = Popup(title="Sorting completed! " + str(self.rounds) + " entries sorted!", content=close, size_hint=(None, None), size=(400, 300))
        close.bind(on_release=self.app.stop)
        popup.open()
        


class FileScreen(BoxLayout):
    def ok_press(self):
        #This is the button to proceed to ChoiceScreen
        #But first, update all info for ParentScreen
        #read mal.csv, add/remove animedict entries accordingly
        try:
            self.parent.score_threshold = int(self.ids['score_diff'].text)
            self.parent.rounds = int(self.ids['rounds'].text)
            self.parent.loadinfo()
        except ValueError:
            close = Button(text='Ok')
            popup = Popup(title="Error: make sure you entered integers", content=close, size_hint=(None, None), size=(400, 300))
            close.bind(on_press=popup.dismiss)
            popup.open()

    def import_press(self):
        filename = self.ids['xmlfile'].text
        if filename[-4:] != ".xml":
            filename += ".xml"
        success = readxml(filename)
        if success:
            close = Button(text='Ok')
            popup = Popup(title=".xml file successfully imported!", content=close, size_hint=(None, None), size=(400, 300))
            close.bind(on_press=popup.dismiss)
            popup.open()
        else:
            close = Button(text='Ok')
            popup = Popup(title=".xml Import Failed!", content=close, size_hint=(None, None), size=(400, 300))
            close.bind(on_press=popup.dismiss)
            popup.open()

class ChoiceScreen(GridLayout):
    leftimg = StringProperty(os.path.join(MAINDIR, "pics", "none.jpg"))
    rightimg = StringProperty(os.path.join(MAINDIR, "pics", "none.jpg"))
    
    def begin(self, anime, sort, unsort, rounds, threshold, parentscreen):
        self.anime = anime
        self.sort = sort
        self.unsort = unsort
        self.threshold = threshold
        self.rounds = rounds
        self.parentscreen = parentscreen
        self.insert()

    def insert(self):
        if (self.rounds > 0) and (self.unsort != []):
            self.rounds -= 1
            self.lefti = 0
            self.righti = len(self.sort)
            self.current = self.unsort[0]
            self.insertstep()
        else:
            self.parentscreen.endchoice()

    def insertstep(self):
        if self.lefti == self.righti:
            self.unsort.pop(0)
            self.sort.insert(self.lefti, self.current)
            self.insert()
        else:
            self.middlei = int((self.lefti + self.righti)//2)
            self.compare_display(self.current,
                            self.sort[self.middlei])
        
    def pressleft(self, *args):
        self.compare(True)

    def pressright(self, *args):
        self.compare(False)

    def compare_display(self, x, y):
        ax = self.anime[x]
        ay = self.anime[y]
        if ax.score != 0 and ay.score != 0:
            if ax.score - ay.score > self.threshold:
                self.compare(False)
                return
            elif ay.score - ax.score > self.threshold:
                self.compare(True)
                return
        self.leftstr = ax.name
        if os.path.isfile(os.path.join(MAINDIR, "pics", ax.idnum + ".jpg")):
            self.leftimg = os.path.join(MAINDIR, "pics", ax.idnum + ".jpg")
        else:
            self.leftimg = os.path.join(MAINDIR, "pics", "none.jpg")
        self.rightstr = ay.name
        if os.path.isfile(os.path.join(MAINDIR, "pics", ay.idnum + ".jpg")):
            self.rightimg = os.path.join(MAINDIR, "pics", ay.idnum + ".jpg")
        else:
            self.rightimg = os.path.join(MAINDIR, "pics", "none.jpg")

    def compare(self, leq):
        if leq:
            self.righti = self.middlei
        else:
            self.lefti = self.middlei + 1
        self.insertstep()
        
        
class MalsortApp(App):
    def build(self):
        return ParentScreen(self)

#Read in the csv created from the xml file
#If getpics, get pictures for anime which don't have pictures yet
#(requires internet, may take time)
def readcsv(getpics):
    animedict = {}
    csv = open(os.path.join(MAINDIR, "mal.csv"), 'r')
    csv.readline()
    for line in csv:
        info = line.split(";")
        if info[1] not in animedict.keys():
            if info[12] != "Completed":
                continue
            if info[9] == '':
                #Ratings of 0 are handled differently in the comparator
                info[9] = 0
            info[1] = namefix(info[1]) + " (" + info[2] + ")"
            animedict[info[0]] = Anime(info[0], info[1], int(info[9]))
        if getpics and (not os.path.isfile(os.path.join(MAINDIR, "pics", info[0] + ".jpg"))):
            #If you don't have an image, get it from MAL
            success = False
            n = 0
            while not success:
                success = lookup(info[0], n)
                n += 1
                if n >= 3: break
            print("Failed to get image for " + info[1])
    csv.close()
    return animedict

def lookup(idnum, n):
    html = urlopen("http://myanimelist.net/anime/" + idnum)
    line = ""
    i = 1
    while (len(line) < 11) or (line[:11] != "    <meta p"):
        line = html.readline()
        i += 1
        if i > 50:
            sleep(n)
            return False
    address = line.split("<meta")[8].split("\"")[3]
    urlretrieve(address, os.path.join(MAINDIR, "pics", idnum + ".jpg"))
    html.close()
    return True

#Since we put the kind in the name anyway, remove redundancies
#(Note: these things aren't likely to occur at the end
# of a title otherwise)
def namefix(title):
    if title[-5:] == "(OVA)":
        return title[:-5]
    elif title[-4:] == "(TV)":
        return title[:-4]
    elif title[-3:] == "OVA":
        return title[:-3]
    elif title[-2:] == "TV":
        return title[:-2]
    else:
        return title

#Gets the currently sorted anime
def readsorted():
    readfile = open(os.path.join(MAINDIR, "sorted.txt"), 'r')
    sortedanime = []
    for line in readfile:
        sortedanime.append(line.strip())
    readfile.close()
    return sortedanime

def writesorted(sortedanime):
    writefile = open(os.path.join(MAINDIR, "sorted.txt"), 'w')
    for idnum in sortedanime:
        writefile.write(idnum + "\n")
    writefile.close()

#Parses the xml file from MAL
def readxml(filename):
    try:
        readfile = open(os.path.join(PARENTDIR, filename), 'r')
        writefile = open(os.path.join(MAINDIR, "mal.csv"), 'w')
        writefile.write('AnimeDB ID; Title; Type; Episodes; '
                        'My ID; Episodes Watched; Start Date; '
                        'Finish Date; Rated; Score; DVD; '
                        'Storage; Status; Comments; Times Watched; '
                        'Rewatch Value; Tags; Rewatching; '
                        'Rewatch Ep; Update on Import\n')
        while True:
            line = readfile.readline()
            if not line: break
            if line.strip() != "<anime>":
                continue
            csvline = ""
            line = readfile.readline()
            while line.strip() != "</anime>":
                line = line.strip()
                tag = re.search('<.*?>', line).group(0)
                content = line[len(tag):-len(tag)-1]
                if len(content) > 8 and content[:8] == "<![CDATA":
                    content = content[9:-3]
                csvline += content.replace(';',':') + ";"
                line = readfile.readline()
            writefile.write(csvline[:-1]+"\n")
        readfile.close()
        writefile.close()
    except IOError:
        return False
    return True


def writeresults(sortedanime, animedict):
    writefile = open(os.path.join(PARENTDIR, "results.txt"), 'w')
    i = 1
    for idnum in sortedanime:
        writefile.write(str(i) + ": " + animedict[idnum].name + "\n")
        i += 1
    writefile.close()
        

if __name__ == '__main__':
    MalsortApp().run()
