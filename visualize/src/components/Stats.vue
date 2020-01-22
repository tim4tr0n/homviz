<template>
  <div class="slidecontainer">
    <h3>Homunculus Stats</h3>
    <hr>
    <p><u>sampled works</u></p>
    <ul>
        <!-- <li>Crime and Punishment</li>
        <li>The Lady with the Dog</li>
        <li>War and Peace</li> -->
        <li v-for="book in books.slice(0,2)" v-bind:key="book.idx">
        {{ book.title }} 
        </li>
    </ul>
    <hr class="sub-breaker">
    <p><u>year range</u></p>
    <h4><b>1840</b> - <b>1920</b></h4>
    <hr class="sub-breaker">
    <p><u>body_state</u></p>
    <h4><b>head</b> <i>0</i></h4>
    <h4><b>hand</b> <i>0</i></h4>
    <h4><b>chest</b> <i>0</i></h4>
    <h4><b>arm</b> <i>0</i></h4>
    <h4><b>foot</b> <i>0</i></h4>
  </div>
</template>

<script>
import Vue from 'vue'
import * as VueWindow from '@hscmap/vue-window'

Vue.use(VueWindow)
import { firebase } from '../firebaseConfig';

export default {
    name: 'Stats',
    data() {
        return {
            sliderValue: null,
            books: [],
            sliderPosition: this.$store.getters.sliderPosition
        }
    },
    firestore() {
        return {
            // books: db.collection('books').where("mouth", ">", 2).orderBy("mouth").limit(5),
            books: firebase.firestore().collection('books').limit(5),
        }
    },
    computed: {
        // TODO : fix these awful naming conventions. will inevitably come when sliderPosition is mapped to homunculus body parts
        slider() {
            return {
                sliderPosition: this.$store.getters.sliderPosition
            }
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .sub-breaker {
        opacity: 0.1
    }
    li {
        color: white
    }
    hr {
        opacity: 0.7
    }
    h3 { 
        color: white
    }
    h4 {
        color: white
    }
    p {
        color: white;
        text-align: left;
        margin-left: 10px;
        
    }
    .slidecontainer {
        width: 20vmax;
        /* height: 35vmax; */
        background: #cccccc;
        background: linear-gradient( rgba(0, 0, 0, 0.25) 100%, #436f7c 100%),
  url('/static/bg.jpg') no-repeat center center fixed;
    }
</style>