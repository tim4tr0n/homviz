import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def uploadFile(filename, db, collectionName, documentName):
    # open file and strip whitespace from ends of each line
    with open(filename) as f:
        lines = [line.strip() for line in f]

    code_meaning_dict = {}
    for line in lines:
        split_line = line.split(' ')
        code = split_line[0] # separate code at beginning of line from the rest of the line
        meaning = line[len(code):]
        code_meaning_dict[code] = meaning.strip() # add the code and it's meaning to the dictionary

    
    # push the dictionary to firebase
    doc_ref = db.collection(collectionName).document(documentName)
    doc_ref.set(code_meaning_dict)

    return code_meaning_dict

# init the firebase API    
cred = credentials.Certificate('serviceAccountKeys/literary-homunculus-7bb1ad294c39.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

print(uploadFile('metadata/classes.txt', db, 'databaseInfo', 'classes'))
print(uploadFile('metadata/languages.txt', db, 'databaseInfo', 'languages'))
print(uploadFile('metadata/subclasses.txt', db, 'databaseInfo', 'subclasses'))