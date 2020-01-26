import Vue from 'vue'
import Vuex from 'vuex'


import { initFirebase, firebase } from '../firebaseConfig';

Vue.use(Vuex)

initFirebase()
  .then( console.log("Firebase initialized!") )
  .catch( err => console.error(err))

const db = firebase.firestore();
async function getBooksBySubject({limit=20,subject="PQ",language="en"}) {
  try {
      var databaseInfoSnapshot = null
      if (subject == null && language == null){
        databaseInfoSnapshot = await db.collection('books').limit(limit).get()
      }
      else if (subject == null){
        databaseInfoSnapshot = await db.collection('books').where("language", "==", language).limit(limit).get()
      }
      else if (language == null){
        databaseInfoSnapshot = await db.collection('books').where("subject", "==", subject).limit(limit).get()
      } else {
        databaseInfoSnapshot = await db.collection('books').where("subject", "==", subject).where("language", "==", language).limit(limit).get()
      }
      console.log("getBooksBySubject", subject)
      console.log("query result size:", databaseInfoSnapshot.size)
      const books = []
      await databaseInfoSnapshot.forEach(doc => {
          // doc.data() is never undefined for query doc snapshots
          // console.log(doc.id, " => ", doc.data());
          books.push(doc.data())
      });
      return books

  } catch (err) {
      console.log("there was an error")
      console.error(err)
  }
}

const storeData = {
  state: {
    bodyState: 3,
    sliderPosition: 0,
    genres: {},
    subgenres: {},
    languages: {},
    selectedGenre: 'P',
    selectedSubgenre: null,
    selectedLanguage: 'en',
    queriedBooks: [],
    witnessedBooks: [],
    selectedBook: null
  },
  mutations: {
    changeSlider(state, value) {
      state.sliderPosition = value
    },
    changeBodyState(state, value) {
      state.bodyState = value
    },
    loadGenres(state, value) {
      state.genres = {...state.genres,...value}
    },
    loadLanguages(state, value) {
      state.languages = {...state.languages,...value}
    },
    loadSubgenres(state, value) {
      state.subgenres = {...state.subgenres,...value}
    },
    changeSelectedGenre(state, value) {
      if(value == "none"){
        state.selectedGenre = null
      } else {
        state.selectedGenre = value;
      }
    },
    changeSelectedSubgenre(state, value) {
      if(value == "none"){
        state.selectedSubgenre = null
      } else {
        state.selectedSubgenre = value
        // console.log("getting fucking books")
        // state.queriedBooks = getBooksBySubject({subject: value})
        // state.witnessedBooks = Array.prototype.push.apply(state.queriedBooks,state.witnessedBooks)
      }
    },
    changeSelectedLanguage(state, value) {
      if(value == "none"){
        state.selectedLanguage = null
      } else {
        state.selectedLanguage = value

      }
    },
    changeQueriedBooks(state, value) {
      state.queriedBooks = value
    },
    changeWitnessedBooks(state,value){
      state.witnessedBooks = Array.prototype.push.apply(value,state.witnessedBooks)
    }
  },
  getters: {
    booksModule: state => state.booksModule,
    bodyState: state => state.bodyState,
    sliderPosition: state => state.sliderPosition,
    genres: state => state.genres,
    subgenres: state => {
      const selectedGenre = state.selectedGenre
      const filtered = Object.keys(state.subgenres)
        .filter(key => key.toLowerCase()[0] == selectedGenre.toLowerCase())
        .reduce((obj, key) => {
          return {
            ...obj,
            [key]: state.subgenres[key]
          };
        }, {});
      return filtered
    },
    selectedGenre: state => state.selectedGenre,
    selectedSubgenre: state => state.selectedSubgenre,
    languages: state => state.languages,
    selectedLanguage: state => state.selectedLanguage,
    queriedBooks: state => state.queriedBooks
  },
  actions: {
    async queryBooks({ commit, getters }) {
      const subject = getters.selectedSubgenre
      const language = getters.selectedLanguage.toLowerCase()
      const books = await getBooksBySubject({limit:50, subject, language})
      console.log(books)
      commit('changeQueriedBooks', books)
      commit('changeWitnessedBooks', books)
    }
  },
  strict: process.env.NODE_ENV !== 'production'
}

export const store = new Vuex.Store(storeData);
  