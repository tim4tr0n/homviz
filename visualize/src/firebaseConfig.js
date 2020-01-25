import { firebase } from "@firebase/app";
import "@firebase/firestore";
import { firebaseConfig } from "./credentials.js";

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