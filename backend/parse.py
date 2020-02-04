import rdflib, wget, re, os, firebase_admin, json, requests, pywikibot
from firebase_admin import credentials
from firebase_admin import firestore

class metadata(object):
    def __init__(self, config_folder_path):
        self.lang_codes_path = config_folder_path + '/lang_codes.txt'
        self.classes_path = config_folder_path + '/classes.txt'
        self.subclasses_path = config_folder_path + '/subclasses.txt'
        self.translation_path = config_folder_path + '/translation.json'
        self.parts_path = config_folder_path + '/parts.csv'

        self.lang_code_dict = self.find_lang_codes()
        self.classes_dict = self.find_classes()
        self.subclasses_dict = self.find_subclasses()

    def parse_two_column(self, path):
        file = open(path, 'r')
        lines = file.readlines()
        file.close()

        dictionary = {}
        for line in lines:
            info_list = line.split(' ')
            dictionary[info_list[0]] = info_list[1].strip('\n')

        return dictionary

    def find_lang_codes(self):
        self.lang_code_dict = self.parse_two_column(self.lang_codes_path)
        return self.lang_code_dict
    
    def find_classes(self):
        self.classes_dict = self.parse_two_column(self.classes_path)
        return self.classes_dict
    
    def find_subclasses(self):
        self.subclasses_dict = self.parse_two_column(self.subclasses_path)
        return self.subclasses_dict

    def find_part_mappings(self):
        file = open(self.parts_path, 'r')
        data = file.readlines()
        file.close()

        # process to list of lists
        parts = [line.strip().strip(',').split(',') for line in data]

        dictionary = {}
        for item in parts:
            targetNameIndex = item.index('targetNames')
            meshesIndex = item.index('meshes')

            part = item[0]
            targetNames = item[targetNameIndex + 1:meshesIndex]
            meshes = item[meshesIndex + 1:]

            part_sub_dictionary = {}
            part_sub_dictionary['meshes'] = meshes
            part_sub_dictionary['targetNames'] = targetNames
            dictionary[part] = part_sub_dictionary

        return dictionary

    def push(self, db, collection='databaseInfo', lang_doc='languages', 
                classes_doc = 'classes', subclasses_doc = 'subclasses', parts_doc = 'bodyParts'):
        lang_doc_ref = db.collection(collection).document(lang_doc)
        lang_doc_ref.set(self.find_lang_codes())

        classes_doc_ref = db.collection(collection).document(classes_doc)
        classes_doc_ref.set(self.find_classes())
        
        subclasses_doc_ref = db.collection(collection).document(subclasses_doc)
        subclasses_doc_ref.set(self.find_subclasses())

        parts_doc_ref = db.collection(collection).document(parts_doc)
        parts_doc_ref.set(self.find_part_mappings())

class book(object):
    def __init__(self, rdf_path, translation_path):
        # file data
        self.rdf_path       = rdf_path
        self.graph          = self.load_rdf(self.rdf_path)
        self.gutenberg_ID   = self.find_id()
        self.gutenberg_source_URL   = self.find_source()
        self.translation_dict_path  = translation_path
        self.translation_dict       = self.load_translation_dict()

        # book metadata
        self.text           = self.download_book()
        self.title          = self.find_title()
        self.author         = self.find_author()
        self.lang_code      = self.find_lang_code()
        self.subject_code   = self.find_subject_code()
        self.publication_date, self.publiction_date_source = None, None

        # processed book data
        self.freq_dict = self.count_words()

    # data ingestion methods
    def load_rdf(self, path):
        """Loads a RDF file from self.rdf_path into a graph, stores the graph
        in the object, and returns the object."""

        self.graph = rdflib.Graph()
        self.graph.load(self.rdf_path)
        return self.graph

    def find_id(self):
        """Returns the ID referenced in project gutenberg of the book."""

        extensionless = self.rdf_path.split(".rdf")[0]
        return int(extensionless.split("catalog/pg")[1])

    def find_source(self):
        """Returns a URL to the raw .txt source on Project Gutenberg for a given catalog file."""

        # generate the subject that we're going to be searching with
        root_subject = rdflib.term.URIRef('http://www.gutenberg.org/ebooks/' + str(self.gutenberg_ID))
        hasFormat_predicate = rdflib.term.URIRef('http://purl.org/dc/terms/hasFormat')
        hasFormat_list = [i for i in self.graph.objects(root_subject, hasFormat_predicate)]
        hasFormat_string_list = [str(i) for i in hasFormat_list]
        resource_list = [i for i in hasFormat_string_list if (('.txt' in i) and ('.txt.utf-8' not in i))]

        if resource_list:
            return resource_list[0]
        
        else:
            return None

    def load_translation_dict(self):
        """Load translation dictionary from the translation and save it to the object."""

        file = open(self.translation_dict_path, 'r')
        word_dict = json.load(file)
        file.close()
        
        return word_dict

    def download_book(self):
        """Downloads the book text and stores it in the book object. Deletes file once done. 
        Returns the text of file, and also stores it in book object"""

        if not self.gutenberg_source_URL: return None #return None immediately if there's no URL for the book

        try:
            wget.download(self.gutenberg_source_URL, str(self.gutenberg_ID), bar=None)

        except KeyboardInterrupt:
            print("Interrupting download, exiting...")
            exit()

        except:
            print("Error in HTTP get for external resource defined by catalog file")
            return None

        
        # if the download was successful, then read it, store its contents, and delete it
        file = open(str(self.gutenberg_ID), 'r', encoding="utf8", errors='ignore')
        self.text = file.read()
        file.close()

        os.remove(str(self.gutenberg_ID))
        return self.text
        

    # metadata extraction methods
    def find_title(self):
        # go find the ID if we don't have it already
        if self.gutenberg_ID == None:
            self.gutenberg_ID = self.find_id()

        # generate the subject that we're going to be searching with
        root_URI = 'http://www.gutenberg.org/ebooks/' + str(self.gutenberg_ID)
        root_subject = rdflib.term.URIRef(root_URI)
        title_predicate = rdflib.term.URIRef('http://purl.org/dc/terms/title')

        # search for the given object given the subject and the predicate
        title_list = []
        for title in self.graph.objects(root_subject, title_predicate):
            title_list.append(title)
        
        if title_list:
            return str(title_list[0])
        return None

    def find_author(self):
        """Returns the author of the book."""

        # generate the subject that we're going to be searching with
        root_URI = 'http://www.gutenberg.org/ebooks/' + str(self.gutenberg_ID)
        root_subject = rdflib.term.URIRef(root_URI)
        
        # find the creator node
        creator_predicate  = rdflib.term.URIRef('http://purl.org/dc/terms/creator')
        creator_list = [i for i in self.graph.objects(root_subject, creator_predicate)]

        if creator_list:
            # now that we have the creator node, we need to find the alias (author) node
            alias_predicate = rdflib.term.URIRef('http://www.gutenberg.org/2009/pgterms/alias')
            alias_list = [i for i in self.graph.objects(creator_list[0], alias_predicate)]
            if len(alias_list) > 0: return str(alias_list[0])

            name_predicate = rdflib.term.URIRef('http://www.gutenberg.org/2009/pgterms/name')
            name_list = [i for i in self.graph.objects(creator_list[0], name_predicate)]
            if len(name_list) > 0: return str(name_list[0])
        
        return None

    def find_lang_code(self):
        """Returns the two-digit language code of the book."""

        # generate the subject that we're going to be searching with
        root_URI = 'http://www.gutenberg.org/ebooks/' + str(self.gutenberg_ID)
        root_subject = rdflib.term.URIRef(root_URI)
        
        # find the creator node
        interstitial_predicate  = rdflib.term.URIRef('http://purl.org/dc/terms/language')
        interstitial_list = [i for i in self.graph.objects(root_subject, interstitial_predicate)]

        subject_list = [i for i in self.graph.predicate_objects(interstitial_list[0])]
        
        return str(subject_list[0][1])

    def find_subject(self):
        """Returns the subject of the book."""

        # generate the subject that we're going to be searching with
        root_URI = 'http://www.gutenberg.org/ebooks/' + str(self.gutenberg_ID)
        root_subject = rdflib.term.URIRef(root_URI)
        
        # we need to the subject of the book
        interstitial_predicate = rdflib.term.URIRef('http://purl.org/dc/terms/subject')
        interstitial_list = [i for i in self.graph.objects(root_subject, interstitial_predicate)]
        if interstitial_list:
            subject_list = [i for i in self.graph.predicate_objects(interstitial_list[0])]    
            linear_subject_list = []
            linear_subject_list.append(subject_list[0][0])
            linear_subject_list.append(subject_list[0][1])
            linear_subject_list.append(subject_list[1][0])
            linear_subject_list.append(subject_list[1][1])
        
            return [str(i) for i in linear_subject_list]
        
        return None

    def find_subject_code(self):
        for _ in range(100):
            if self.find_subject():
                for subject in self.find_subject():
                    if len(subject) == 2:
                        return subject

        return None

    def find_publication_date_Wikipedia(self):
        try:
            site = pywikibot.Site("en", "wikipedia")
            page = pywikibot.Page(site, self.title)
            item = pywikibot.ItemPage.fromPage(page)
            dictionary = item.get()
            clm_dict = dictionary["claims"]
            clm_list = clm_dict["P577"]
            year = None
            for clm in clm_list:
                clm_trgt = clm.getTarget()
                year = clm_trgt.year
        except (KeyError):
            try:
                return self.find_publication_date_Wikipedia(self.title + " (novel)")
            except pywikibot.exceptions.NoPage:
                return None
        except pywikibot.exceptions.NoPage:
            try:
                if self.title == self.title.split(":", 1)[0].split(";,1")[0]:
                    return None
                else:
                    return self.find_publication_date_Wikipedia(author, title.split(":", 1)[0].split(";,1")[0])
            except pywikibot.exceptions.NoPage:
                return None
        except pywikibot.exceptions.InvalidTitle:
            return None
        return year

    def find_publication_date_Google_Books(self):
        # query Google books for the author and 
        payload = {'q':self.title, 'inAuthor':self.author}
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

    def find_publication_date_Copyright(self):
        if self.text:
            match = re.search(r"(COPYRIGHT,?\s*) (\d{4})", self.text, flags = re.IGNORECASE)
            if match:
                return int(match.group(2))
            else:
                return None
        return None

    def find_publication_date(self):
        """Determines the publication date of a book by checking the copyright information
        in the book header, Wikipedia data, and Google Books data"""

        date_dict = {'copyright': self.find_publication_date_Copyright(),
                     'Google Books':self.find_publication_date_Google_Books(),
                     'Wikipedia':self.find_publication_date_Wikipedia()}

        return min(date_dict, key=date_dict.get), date_dict[min(date_dict, key=date_dict.get)]

    # processing methods
    def count_words(self):
        """Takes in a path to a .txt file and a dictionary of body part words,
        and returns a dictionary of each word and how often it occurs."""

        # select proper dictionary to use
        # (if the two character language code is already stored in the book object, use it)
        # (if not, then parse the book to find it
        if self.lang_code == None:
            self.lang_code = self.find_lang_code()

        # check that our .json wordlist has an entry for the language we want
        lang_dict = {}
        if self.lang_code in self.translation_dict.keys():
            lang_dict = self.translation_dict[self.lang_code]
        
        else:
            print("Warning! Text is of language", self.lang_code, "which is not in the wordlist!")
            return {}

        frequency_dict = {}
        book_words = re.split(r"""[-.!;',~:\s]\s*""", str(self.text)) # remove punctuation from the book, and split into a list of words

        for word in book_words:
            if word in lang_dict.keys(): #if the word is recognized as a body part word, add it to the dictionary
                english_equivalent = lang_dict[word]

                # if it's in the dictionary, just add one to the frequency
                if english_equivalent in frequency_dict.keys():
                    frequency_dict[english_equivalent] += 1
                
                # otherwise, add itself to the dictionary
                else:
                    frequency_dict[english_equivalent] = 1
            

        return frequency_dict

    def display(self):
        print("============================")
        print("file data:")
        print("  rdf path:", self.rdf_path)
        print("  gutenberg ID:", self.gutenberg_ID)
        print("  source URL: ", self.gutenberg_source_URL)
        print("  translation dict path:", self.translation_dict_path)

        print("\nbook data:")
        print("  length:", len(self.text), "characters")
        print("  title:", self.title)
        print("  author:", self.author)
        print("  lang:", self.lang_code)
        print("  subject:", self.subject_code)
        print("  pub date:", self.publication_date)

    def asdict(self):
        book_dict = {
            'author' : self.author,
            'title' : self.title,
            'language' : self.lang_code,
            'subject' : self.subject_code,
            'id' : self.gutenberg_ID,
            'publicationDate' : self.publication_date,
            'publlicationDateSource' : self.publiction_date_source
        }
        
        book_dict.update(self.freq_dict)
        return book_dict

    def push(self, db, collection='databaseInfo'):
        '''Pushes book to given db, but only if it contains any words/meaningful data.'''

        if self.freq_dict:
            doc_ref = db.collection(collection).document(str(self.gutenberg_ID))
            doc_ref.set(self.asdict())

        else:
            print('Book does not reference any body parts! What a sad excuse for a book.')


translation_dict_path = "config/translation.json" # load translation file

# get list of all files in directory
catalog_files = sorted([('catalog/' + f) for f in os.listdir('catalog/') if os.path.isfile(os.path.join('catalog/', f))])

# init firebase client
cred = credentials.Certificate('serviceAccountKeys/literary-homunculus-7bb1ad294c39.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# push metadata to firebase
meta = metadata('config/')
meta.push(db)

# push book data to firebase
for catalog_file in catalog_files[1:]:
    current_book = book(catalog_file, translation_dict_path)
    current_book.push(db)
    print(catalog_file)