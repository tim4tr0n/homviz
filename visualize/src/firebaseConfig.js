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
// firebase.initializeApp(firebaseConfig);
// TODO figure out how to properly implement analytics
// firebase.analytics();

function initFirebase () {
    firebase.initializeApp(firebaseConfig);
    return new Promise((resolve, reject) => {
        firebase.firestore().enablePersistence()
        .then(resolve)
        .catch(err => {
            if (err.code === 'failed-precondition') {
            reject(err)
            // Multiple tabs open, persistence can only be
            // enabled in one tab at a a time.
            } else if (err.code === 'unimplemented') {
            reject(err)
            // The current browser does not support all of
            // the features required to enable persistence
            }
        })
    })
}


export {
    firebase,
    initFirebase
}