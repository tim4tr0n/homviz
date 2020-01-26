import rdflib, wget, re, os, firebase_admin, json, requests
from firebase_admin import credentials
from firebase_admin import firestore

def loadRDF(path):
    """Loads a RDF file from the path into a graph, and returns the graph"""
    g = rdflib.Graph()
    g.load(path)
    return g

def findID(path):
    """Returns the ID of the book with given path."""
    extensionless = path.split(".rdf")[0]
    return extensionless.split("catalog/pg")[1]

def downloadBook(path):
    """Downloads the book given by the catalog file."""
    bookID = findID(path)
    source = findSource(path)

    if source:
        try:
            wget.download(source, str(bookID) + '.txt', bar=None)
        
        except KeyboardInterrupt:
            exit()

        except:
            print("Error in HTTP get for external resource defined by catalog file", path)
            return None

        else:
            return (str(bookID) + '.txt')
    else:
        return None

def findTitle(path):
    bookID = findID(path)
    graph = loadRDF(path)

    # generate the subject that we're going to be searching with
    root_URI = 'http://www.gutenberg.org/ebooks/' + bookID
    root_subject = rdflib.term.URIRef(root_URI)
    title_predicate = rdflib.term.URIRef('http://purl.org/dc/terms/title')

    # search for the given object given the subject and the predicate
    title_list = []
    for title in graph.objects(root_subject, title_predicate):
        title_list.append(title)
    
    return str(title_list[0])

def findAuthor(path):
    """Returns the author of the book with the given path."""
    bookID = findID(path)
    graph = loadRDF(path)

    # generate the subject that we're going to be searching with
    root_URI = 'http://www.gutenberg.org/ebooks/' + bookID
    root_subject = rdflib.term.URIRef(root_URI)
    
    # find the creator node
    creator_predicate  = rdflib.term.URIRef('http://purl.org/dc/terms/creator')
    creator_list = [i for i in graph.objects(root_subject, creator_predicate)]

    if creator_list:
        # now that we have the creator node, we need to find the alias (author) node
        alias_predicate = rdflib.term.URIRef('http://www.gutenberg.org/2009/pgterms/alias')
        alias_list = [i for i in graph.objects(creator_list[0], alias_predicate)]
        if len(alias_list) > 0: return str(alias_list[0])

        name_predicate = rdflib.term.URIRef('http://www.gutenberg.org/2009/pgterms/name')
        name_list = [i for i in graph.objects(creator_list[0], name_predicate)]
        if len(name_list) > 0: return str(name_list[0])
    
    return None

def findSource(path):
    """Returns a URL to the raw .txt source on Project Gutenberg for a given catalog file."""
    bookID = findID(path)
    graph = loadRDF(path)

    # generate the subject that we're going to be searching with
    root_subject = rdflib.term.URIRef('http://www.gutenberg.org/ebooks/' + bookID)
    hasFormat_predicate = rdflib.term.URIRef('http://purl.org/dc/terms/hasFormat')
    hasFormat_list = [i for i in graph.objects(root_subject, hasFormat_predicate)]
    hasFormat_string_list = [str(i) for i in hasFormat_list]
    resource_list = [i for i in hasFormat_string_list if (('.txt' in i) and ('.txt.utf-8' not in i))]

    if resource_list:
        return resource_list[0]
    
    else:
        return None

def findLanguage(path):
    """Returns the author of the book with the given path."""
    bookID = findID(path)
    graph = loadRDF(path)

    # generate the subject that we're going to be searching with
    root_URI = 'http://www.gutenberg.org/ebooks/' + bookID
    root_subject = rdflib.term.URIRef(root_URI)
    
    # find the creator node
    interstitial_predicate  = rdflib.term.URIRef('http://purl.org/dc/terms/language')
    interstitial_list = [i for i in graph.objects(root_subject, interstitial_predicate)]

    subject_list = [i for i in graph.predicate_objects(interstitial_list[0])]
    
    return str(subject_list[0][1])

def findSubject(path):
    """Returns the subject of the book with the given path"""
    bookID = findID(path)
    graph = loadRDF(path)

    # generate the subject that we're going to be searching with
    root_URI = 'http://www.gutenberg.org/ebooks/' + bookID
    root_subject = rdflib.term.URIRef(root_URI)
    
    # we need to the subject of the book
    interstitial_predicate = rdflib.term.URIRef('http://purl.org/dc/terms/subject')
    interstitial_list = [i for i in graph.objects(root_subject, interstitial_predicate)]
    if interstitial_list:
        subject_list = [i for i in graph.predicate_objects(interstitial_list[0])]    
        linear_subject_list = []
        linear_subject_list.append(subject_list[0][0])
        linear_subject_list.append(subject_list[0][1])
        linear_subject_list.append(subject_list[1][0])
        linear_subject_list.append(subject_list[1][1])
    
        return [str(i) for i in linear_subject_list]
    
    return []

def findSubjectCode(path):
    for _ in range(100):
        for subject in findSubject(path):
            if len(subject) == 2:
                return subject

    return None

def findPublicationDate(path):
    # query Google books for the author and 
    payload = {'q':findTitle(path), 'inAuthor':findAuthor(path)}

    r = requests.get('https://www.googleapis.com/books/v1/volumes?', params = payload)

    # make sure that the query didn't fail
    if r.status_code != 200:
        raise RuntimeError('Unable to find Google Books Data, got HTTP status ' + str(r.status_code))

    # we want to find the earliest entry in the list
    # we do this by making a dictionary of every entry that Google returned, and finding the entry with the earliest date
    raw = r.json()
    date_dict = {}
    for index in range(len(raw['items'])):
        date_dict[index] = raw['items'][index]['volumeInfo']['publishedDate'][:4]
    
    min_index = min(date_dict, key=date_dict.get)

    return raw['items'][min_index]['volumeInfo']['publishedDate']


def getWordDict(path):
    """Takes in a path to a .json file containing all the words
    that mean body parts in a bunch of languages, returns a
    dictonary of languages, words, and their english equivalents."""

    file = open(path, 'r')
    word_dict = json.load(file)
    file.close()
    
    return word_dict

def countWords(book_path, book_dict, wordlist_dict):
    """Takes in a path to a .txt file and a dictionary of body part words,
    and returns a dictionary of each word and how often it occurs."""

    # open book file and read to file
    file = open(book_path, encoding="utf8", errors='ignore')
    book = file.read()
    file.close()
    
    # remove punctuation from the book, and split into a list of words
    book_words = re.split(r"""[-.!;',~:\s]\s*""", book)

    # select proper dictionary to use
    # (if the two character language code is already stored in the book dictionary, use it)
    # (if not, then parse the book to find it)
    lang_dict = {}

    if 'language' in book_dict.keys():
        lang_code = book_dict['language']
    
    else:
        lang_code = findLanguage(book_path)

    # check that our .json wordlist has an entry for the language we want
    if lang_code in wordlist_dict.keys():
        lang_dict = wordlist_dict[lang_code]
    
    else:
        print("Warning! Text is of language", lang_code, "which is not in the wordlist!")
        return None
    
    # we now have a dictionary specific to the language of the book we're parsing, so let's parse the book
    for word in book_words:
        if word in lang_dict.keys(): #if the word is recognized as a body part word, add it to the dictionary
            english_equivalent = lang_dict[word]

            # if it's in the dictionary, just add one to the frequency
            if english_equivalent in book_dict.keys():
                book_dict[english_equivalent] += 1
            
            # otherwise, add itself to the dictionary
            else:
                book_dict[english_equivalent] = 1
         

    return book_dict

def createBookDict(rdf_path, wordlist_dict):
    book_path = downloadBook(rdf_path)
    
    if book_path == None:
        print("Warning! No external resource candidate found for file", rdf_path)
        return None

    else:
        book_dict = {
            'title' : findTitle(rdf_path),
            'author' : findAuthor(rdf_path),
            'source' : findSource(rdf_path),
            'language' : findLanguage(rdf_path),
            'subject' : findSubjectCode(rdf_path),
            'id' : findID(rdf_path)
            #'publishedDate' : findPublicationDate(rdf_path)
        }

        countWords(book_path, book_dict, wordlist_dict)
        os.remove(book_path)
        return book_dict

# load file
wordlist_path = "metadata/wordlist.json"
wordlist_dict = getWordDict(wordlist_path)

# get list of all files in directory
catalog_files = sorted([('catalog/' + f) for f in os.listdir('catalog/') if os.path.isfile(os.path.join('catalog/', f))])

# Use a service account
cred = credentials.Certificate('serviceAccountKeys/literary-homunculus-7bb1ad294c39.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

for catalog_file in catalog_files:
    book_dict = createBookDict(catalog_file, wordlist_dict)
    if book_dict:
        doc_ref = db.collection(u'books').document(book_dict['id'])    
        doc_ref.set(book_dict)
        print(catalog_file)
    