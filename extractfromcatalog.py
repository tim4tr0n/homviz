import rdflib, wget, re, os, firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def loadRDF(path):
    """Loads a RDF file from the path into a graph, and returns the graph"""
    g = rdflib.Graph()
    g.load(path)
    return g

def findTitle(path):
    """Returns the title of the book with the given path."""
    extensionless = path.split(".rdf")[0]
    bookID = extensionless.split("catalog/pg")[1]

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
    extensionless = path.split(".rdf")[0]
    bookID = extensionless.split("catalog/pg")[1]

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

def findSubject(path):
    """Returns the subject of the book with the given path"""
    extensionless = path.split(".rdf")[0]
    bookID = extensionless.split("catalog/pg")[1]

    graph = loadRDF(path)

    # generate the subject that we're going to be searching with
    root_URI = 'http://www.gutenberg.org/ebooks/' + bookID
    root_subject = rdflib.term.URIRef(root_URI)
    
    # we need to the subject of the book
    interstitial_predicate = rdflib.term.URIRef('http://purl.org/dc/terms/subject')
    interstitial_list = [i for i in graph.objects(root_subject, interstitial_predicate)]
    subject_list = [i for i in graph.predicate_objects(interstitial_list[0])]

    
    linear_subject_list = []
    linear_subject_list.append(subject_list[0][0])
    linear_subject_list.append(subject_list[0][1])
    linear_subject_list.append(subject_list[1][0])
    linear_subject_list.append(subject_list[1][1])
    
    return [str(i) for i in linear_subject_list]

def findSubjectCode(path):
    while True:
        for subject in findSubject(path):
            if len(subject) == 2:
                return subject

def downloadBook(path):
    """Downloads the book given by the catalog file."""
    extensionless = path.split(".rdf")[0]
    bookID = extensionless.split("catalog/pg")[1]

    graph = loadRDF(path)

    # generate the subject that we're going to be searching with
    root_subject = rdflib.term.URIRef('http://www.gutenberg.org/ebooks/' + bookID)
    hasFormat_predicate = rdflib.term.URIRef('http://purl.org/dc/terms/hasFormat')
    hasFormat_list = [i for i in graph.objects(root_subject, hasFormat_predicate)]
    hasFormat_string_list = [str(i) for i in hasFormat_list]
    resource_list = [i for i in hasFormat_string_list if (('.txt' in i) and ('.txt.utf-8' not in i))]

    if resource_list != []:
        try:
            wget.download(resource_list[0], str(bookID) + '.txt', bar=None)
        
        except KeyboardInterrupt:
            exit()

        except:
            print("Error in HTTP get for external resource defined by catalog file", path)
            return None

        else:
            return (str(bookID) + '.txt')
    else:
        return None

def getWordList(path):
    """Takes in a path to a .txt containing all the words that
    mean body parts in English, returns a list of words."""

    file = open(path, 'r')
    body_part_word_list = file.readlines()
    file.close()

    for i in range(len(body_part_word_list)):
        word = body_part_word_list[i]
        body_part_word_list[i] = word.split('\n')[0]
    
    return body_part_word_list

def countWords(book_path, body_part_word_list):
    """Takes in a path to a .txt file and a list of body part words,
    and returns a dictionary of each word and how often it occurs."""

    file = open(book_path, encoding="utf8", errors='ignore')
    book = file.read()
    file.close()
    
    book_words = re.split(r"""[-.!;',~:\s]\s*""", book)
    frequency_dict = {}

    for word in book_words:
        word = word.lower()

        if word in body_part_word_list:
            if word in frequency_dict.keys():
                frequency_dict[word] += 1
            else:
                frequency_dict[word] = 1
    
    return frequency_dict

def createBookDict(rdf_path):
    book_path = downloadBook(rdf_path)
    temp_dict = {}
    
    if book_path == None:
        print("Warning! No external resource candidate found for file", rdf_path)

    else:
        temp_dict = countWords(book_path, body_part_word_list)
        os.remove(book_path)

        temp_dict['title'] = findTitle(rdf_path)
        temp_dict['author'] = findAuthor(rdf_path)
        #temp_dict['subject'] = findSubjectCode(rdf_path)

        extensionless = rdf_path.split(".rdf")[0]
        temp_dict['id'] = extensionless.split("catalog/pg")[1]

    return temp_dict


# load file
wordlist_path = "wordlist.txt"
body_part_word_list = getWordList(wordlist_path)

# get list of all files in directory
catalog_files = sorted([('catalog/' + f) for f in os.listdir('catalog/') if os.path.isfile(os.path.join('catalog/', f))])

# Use a service account
cred = credentials.Certificate('serviceAccountKeys/literary-homunculus-7bb1ad294c39.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

for catalog_file in catalog_files:
    book_dict = createBookDict(catalog_file)
    
    if book_dict:
        doc_ref = db.collection(u'books').document(book_dict['id'])    
        doc_ref.set(book_dict)
        print(catalog_file)
    