# malsort
Sort your My Anime List list manually (in case you don't think number ratings are good enough)

How to use:
First you need an xml file containing the information from your MAL, which you can get at
https://myanimelist.net/panel.php?go=export

Unzip this file, rename it if you like (but keep the .xml extension), and place it in the parent directory of the directory containing malsort.py.  This parent directory is also where results will be printed.

Run malsort.py (or malsort.exe, in a windows build) and import your .xml file using the top button.

You can also choose the "score threshold": you won't be asked to compare items more than N apart in score (according to the scores you gave them on your MAL).  For instance, if you set this number to 1, then an 8 will automatically be determined to be better than a 6, but you'll be asked to compare an 8 against a 7.

Finally, choose the number of items you want to sort.  You don't have to do them all at once, but your results won't be saved unless you finish the batch.  They are stored internally in sorted.txt, but a more readable version will be produced in the parent folder, called results.txt.



You can later reimport your list data, and any previous sorting you did will be preserved, as long as the items are still on your list.  However, any entries which are no longer present on your list will be removed.

If you want to reset the sorting, you can either delete all the data in sorted.txt, or import a completely blank .xml document (of course, you then need to "sort" the empty data to have it be saved).

Pictures will automatically be pulled from myanimelist as needed.  A rather large, but far from exhaustive, collection of such pictures is already included.

These pictures aren't necessary, but you do need to have a picture called "pics/none.jpg" to fill in for images (this is included in the pics folder).

Made by Chris Hunt
7.27.2017
huntchristopher2012@gmail.com