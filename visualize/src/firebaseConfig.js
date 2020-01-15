import { firebase } from "@firebase/app";
import "@firebase/firestore";

const firebaseConfig = {
    apiKey: "AIzaSyAdQz2qqdz8pSg5EL5WnPtOWm_jZ_-fmbE",
    authDomain: "literary-homunculus.firebaseapp.com",
    databaseURL: "https://literary-homunculus.firebaseio.com",
    projectId: "literary-homunculus",
    storageBucket: "literary-homunculus.appspot.com",
    messagingSenderId: "243950825999",
    appId: "1:243950825999:web:30bfb362c02058c472697a",
    measurementId: "G-CKCPFJNTGZ"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
// TODO figure out how to properly implement analytics
// firebase.analytics();

const db = firebase.firestore();

const booksCollection = db.collection('books');

export {
    db,
    booksCollection
}