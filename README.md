# The Literary Homunculus
The Homunculus Visualizer -- work in progress ;)

Repository Contents
-------------------

* **pullcatalog.sh** - Downloads the catalog from Project Gutenberg, and creates a catalog/ directory with a catalog file for every book. 
* **extractfromcatalog.py** - Goes thorugh every file in the catalog to download the book, parse it, and upload the results to Firebase.
* **wordlist.txt**  - List of words of interest that will be counted and put in Firebase. 
* **/serviceAccountKeys**  - Stores the .json private keys associated with the service account that updates Firebase.
* **/visualize** - Luke and Keith do magic here. That is all you need to know.

