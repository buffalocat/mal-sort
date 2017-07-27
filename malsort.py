#!/usr/bin/env python
### Let's make a GUI

import kivy
from random import (random, shuffle)

class MergeNode:
    def __init__(self, arr):
        n = len(arr)
        if n <= 1:
            self.value = arr
            self.left  = 0
            self.right = 0
            self.isSorted = True
        else:
            k = n//2
            self.value = []
            self.left  = MergeNode(arr[:k])
            self.right = MergeNode(arr[k:])
            self.isSorted = False
    
    def compare_ask(self, screen):
        #randomly pick which side to check first
        if random() < 0.5:
            if not self.left.isSorted:
                self.left.compare_ask(screen)
            elif not self.right.isSorted:
                self.right.compare_ask(screen)
            #if both sides are sorted, do a compare
            else:
                screen.compare_display(self.left.value[0],
                                       self.right.value[0], self)
        else:
            if not self.right.isSorted:
                self.right.compare_ask(screen)
            elif not self.left.isSorted:
                self.left.compare_ask(screen)
            #if both sides are sorted, do a compare
            else:
                screen.compare_display(self.left.value[0],
                                       self.right.value[0], self)
                
    def compare(self, leq):
        if leq:
            self.value.append(self.left.value.pop(0))
            if len(self.left.value) == 0:
                self.value += self.right.value
                self.isSorted = True
        else:
            self.value.append(self.right.value.pop(0))
            if len(self.right.value) == 0:
                self.value += self.left.value
                self.isSorted = True
        if self.isSorted:
            self.left = 0
            self.right = 0

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
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.properties import NumericProperty

class ParentScreen(BoxLayout):
    arr = ListProperty([])
    score_threshold = 0
    
    def __init__(self, **kwargs):
        super(ParentScreen, self).__init__(**kwargs)
        self.screen = FileScreen()
        self.add_widget(self.screen)

    def ready(self):
        self.remove_widget(self.screen)
        self.screen = ChoiceScreen()
        self.screen.begin(self.arr, self.score_threshold)
        self.add_widget(self.screen)
        
    def result(self, arr):
        self.remove_widget(self.screen)
        write(arr)
        self.add_widget(Label(text="Sorting Complete! Results written to results.txt"))


class FileScreen(BoxLayout):
    def press(self):
        self.parent.arr = read()
        self.parent.score_threshold = int(self.ids['score_diff'].text)
        self.parent.ready()


class ChoiceScreen(GridLayout):   
    curnode  = ObjectProperty(MergeNode([]))
    arr = []
    
    def __init__(self, **kwargs):
        super(ChoiceScreen, self).__init__(**kwargs)
        self.rootnode = ObjectProperty(MergeNode(self.arr))

    def begin(self, arr, score_threshold):
        self.score_threshold = score_threshold
        self.rootnode = MergeNode(arr)
        self.askroot()

    def pressleft(self, *args):
        self.curnode.compare(True)
        self.askroot()

    def pressright(self, *args):
        self.curnode.compare(False)
        self.askroot()

    def compare_display(self, x, y, node):
        self.curnode = node
        if x.score != 0 and y.score != 0:
            if x.score - y.score > self.score_threshold:
                node.compare(False)
                self.askroot()
                return
            elif y.score - x.score > self.score_threshold:
                node.compare(True)
                self.askroot()
                return
        self.leftstr = x.name
        self.leftimg = "pics/" + x.idnum + ".jpg"
        self.rightstr = y.name
        self.rightimg = "pics/" + y.idnum + ".jpg"
        
    def askroot(self):
        if self.rootnode.isSorted:
            self.parent.result(self.rootnode.value)
        else:
            self.rootnode.compare_ask(self)
        
        
class MalsortApp(App):
    def build(self):
        return ParentScreen()

                
def read():
    arr = []
    csv = open("ccmal.csv", 'r')
    csv.readline()
    for line in csv:
        info = line.split(";")
        if info[12] != "Completed":
            continue
        if info[9] == '':
            #Ratings of 0 are handled differently in the comparator
            info[9] = 0
        info[1] = namefix(info[1]) + " (" + info[2] + ")"
        arr.append(Anime(info[0], info[1], int(info[9])))
    shuffle(arr)
    csv.close()
    return arr[:8]

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
    
def write(arr):
    writefile = open("../results.txt", 'w')
    i = 1
    for a in arr:
        writefile.write(str(i) + ": " + a.name + "\n")
        i += 1
    writefile.close()
        

if __name__ == '__main__':
    MalsortApp().run()
