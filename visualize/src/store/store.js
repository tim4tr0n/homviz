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
          const book = {...doc.data(), selected: false}
          books.push(book)
      });
      return books

  } catch (err) {
      console.log("there was an error")
      console.error(err)
  }
}

const storeData = {
  state: {
    bodyState: {},
    homunculusState: {},
    sliderPosition: 0,
    genres: {},
    subgenres: {},
    languages: {},
    bodyParts: [],
    selectedGenre: 'P',
    selectedSubgenre: null,
    selectedLanguage: 'en',
    queriedBooks: [],
    selectedBook: null,
    selectedBookIndex: 0, // this is tricky. we should probably reset the selected book every time a new query happens in order to avoid issues with this
  },
  mutations: {
    changeSlider(state, value) {
      state.sliderPosition = value
    },
    changeBodyState(state, value) {
      state.bodyState = value
    },
    changeHomunculusState(state, value){
      state.homunculusState = value
    },
    changeHomunculusPartByIndex(state, value){ // this is here only to prevent bugs and shit - delete for production
      const sliderValue = value.sliderValue/100
      state.homunculusState["thigh"] = sliderValue
    },
    changeHomunculusPartByScheme(state, value){ // this is here only to prevent bugs and shit - delete for production
      const sliderValue = value.sliderValue/100
      state.homunculusState["thigh"] = sliderValue
    },
    changeHomunculusPartState(state, value){
      const part = value.part
      const sliderValue = value.sliderValue/100
      state.homunculusState[part] = sliderValue
    },
    loadBodyParts(state, value) {
      state.bodyParts = value
    },
    loadHomunculusState(state, value) {
      state.homunculusState = value
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
      }
    },
    changeSelectedLanguage(state, value) {
      if(value == "none"){
        state.selectedLanguage = null
      } else {
        state.selectedLanguage = value

      }
    },
    changeSelectedBook(state, value){
      state.selectedBook = value
    },
    changeSelectedBookIndex(state, value){
      state.selectedBookIndex = value
    },
    changeQueriedBooks(state, value) {
      state.queriedBooks = value
    }
  },
  getters: {
    booksModule: state => state.booksModule,
    homunculusState: state => state.homunculusState,
    bodyState: state => state.bodyState,
    bodyParts: state => state.bodyParts,
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
    languages: state => state.languages,
    selectedGenre: state => state.selectedGenre,
    selectedSubgenre: state => state.selectedSubgenre,
    selectedLanguage: state => state.selectedLanguage,
    selectedBook: state => state.selectedBook,
    selectedBookIndex: state => state.selectedBookIndex,
    queriedBooks: state => state.queriedBooks
  },
  actions: {
    async queryBooks({ commit, getters }) {
      const subject = getters.selectedSubgenre
      const language = getters.selectedLanguage.toLowerCase()
      const books = await getBooksBySubject({limit:50, subject, language})
      console.log("new books have been loaded in", books)
      commit('changeQueriedBooks', books)
    },
    changeSelectedBookAndBodyState({ commit, getters}, value) {
      const selectedBook = value.book;
      const index = value.index;
      const bodyParts  = getters.bodyParts;
      const homunculusState = getters.homunculusState; // fishy way to get our desired list of body parts. consider more deeply
      const bookBodyParts = Object.keys(selectedBook) // this name is not the best. we're getting the keys of the selected book object that are body parts
          .filter(key => key in bodyParts)
          .reduce((obj, key) => {
              return {
                  ...obj,
                  [key]: selectedBook[key]
              };
          }, {});
      
      const changedHomunculusState = Object.keys(bookBodyParts)
          .filter(key => key in homunculusState) // figure out how to deal with plurals / synonyms here
          .reduce((obj, key) => {
              return {
                  ...obj,
                  [key]: bookBodyParts[key]
              };
          }, {});
      
      console.log("CHANGED HOMUNCULUS OBJECT", changedHomunculusState)
      const mergedHomunculusState = {...homunculusState, ...changedHomunculusState} // this is shitty because it accumulates over time. need to reset each time god dammit
      commit("changeHomunculusState", mergedHomunculusState)
      commit("changeSelectedBook", selectedBook)
      commit("changeSelectedBookIndex", index)
      commit("changeBodyState", bookBodyParts)
    }
  },
  strict: process.env.NODE_ENV !== 'production'
}

export const store = new Vuex.Store(storeData);
