import Vue from 'vue'
import Vuex from 'vuex'


import { initFirebase, firebase } from '../firebaseConfig';

Vue.use(Vuex)

initFirebase()
  .then( console.log("Firebase initialized!") )
  .catch( err => console.error(err))

const db = firebase.firestore();
async function getBooksBySubject({limit=20,subject="PQ",language="en",byYear=false}) {
  try {
      var databaseInfoSnapshot = null
      store.commit("changeLoadingStatus", true)
      if (byYear) {
        console.log("querying by year")
        
        if (subject == null && language == null){
          databaseInfoSnapshot = await db.collection('books').limit(limit).where('publicationDate', '>=', 0).get()
        }
        else if (subject == null){
          console.log("actually in here")
          databaseInfoSnapshot = await db.collection('books').limit(limit).where("language", "==", language).where('publicationDate', '>=', 0).get()
        }
        else if (language == null){
          databaseInfoSnapshot = await db.collection('books').limit(limit).where("subject", "==", subject).where('publicationDate', '>=', 0).get()
        } else {
          console.log("we're in here")
          console.log("subject", subject)
          console.log("language", language)
          databaseInfoSnapshot = await db.collection('books').limit(limit).where("subject", "==", subject).where("language", "==", language).where('publicationDate', '>=', 0).get()
        }
      }
      else if (subject == null && language == null){
        databaseInfoSnapshot = await db.collection('books').limit(limit).get()
      }
      else if (subject == null){
        databaseInfoSnapshot = await db.collection('books').limit(limit).where("language", "==", language).get()
      }
      else if (language == null){
        databaseInfoSnapshot = await db.collection('books').limit(limit).where("subject", "==", subject).get()
      } else {
        databaseInfoSnapshot = await db.collection('books').limit(limit).where("subject", "==", subject).where("language", "==", language).get()
      }
      console.log("we're done loading this shit")
      store.commit("changeLoadingStatus", false)
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
    loadingBooks: false,
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
    viewByYearMode: false,
    latestYear: null,
    earliestYear: null
  },
  mutations: {
    changeLoadingStatus(state, value){
      state.loadingBooks = value
    },
    changeViewByYearMode(state, value){
      state.viewByYearMode = value
    },
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
      const queriedBooks = value
      const viewByYearMode = state.viewByYearMode
      if (viewByYearMode){
        console.log("populating by year too")
        state.earliestYear = queriedBooks[0].publicationDate
        state.latestYear = queriedBooks[queriedBooks.length  - 1].publicationDate
      }
      
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
    queriedBooks: state => state.queriedBooks,
    loadingBooks: state => state.loadingBooks,
    viewByYearMode: state => state.viewByYearMode,
    earliestYear: state => state.earliestYear,
    latestYear: state => state.latestYear
  },
  actions: {
    async queryBooks({ commit, getters }) {
      const subject = getters.selectedSubgenre
      const language = getters.selectedLanguage.toLowerCase()
      const byYear = getters.viewByYearMode
      const books = await getBooksBySubject({limit:50, subject, language, byYear})
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
      const resetHomunculusState = Object.keys(homunculusState) // very unelegant way to reset the shape -> maybe add option to accumulate!!!
          .filter(key => key in homunculusState)
          .reduce((obj, key) => {
              return {
                  ...obj,
                  [key]: 0
              };
          }, {});
      
      const mergedHomunculusState = {...resetHomunculusState, ...bookBodyParts} 
      commit("changeHomunculusState", mergedHomunculusState)
      commit("changeSelectedBook", selectedBook)
      commit("changeSelectedBookIndex", index)
      commit("changeBodyState", bookBodyParts)
    }
  },
  strict: process.env.NODE_ENV !== 'production'
}

export const store = new Vuex.Store(storeData);
