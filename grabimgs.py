from urllib import (urlopen, urlretrieve)
from time import sleep

def lookup(idnum):
    html = urlopen("http://myanimelist.net/anime/" + idnum)
    line = ""
    i = 1
    while (len(line) < 11) or (line[:11] != "    <meta p"):
        line = html.readline()
        i += 1
        if i > 25:
            print("Tried to get " + idnum)
            return False
    address = line.split("<meta")[8].split("\"")[3]
    urlretrieve(address, "pics/" + idnum + ".jpg")
    html.close()
    return True

if __name__ == "__main__":
    csv = open("ccmal.csv", 'r')
    n = 0
    for i in range(148):
        csv.readline()
        n += 1
    for line in csv:
        idnum = line.split(";")[0]
        done = False
        while not done:
            sleep(3)
            done = lookup(idnum)
        n += 1
        print(idnum + ": GET " + str(n))
    csv.close()
