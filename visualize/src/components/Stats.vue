<template>
  <div class="slidecontainer">
    <h3>Homunculus Stats</h3>
    <hr>
    <p><u>sampled works</u>: <i>({{stats.queriedBooks.length}} books queried)</i></p>
    <div class="bookscontainer">
        <!-- <li>Crime and Punishment</li>
        <li>The Lady with the Dog</li>
        <li>War and Peace</li> -->
        <!-- <virtual-list :size="40" :remain="8">
            <item v-for="book in stats.queriedBooks" :key="book.idx"/>
        </virtual-list> -->
        <div v-if="stats.queriedBooks.length == 0" class="defaultstats">
            <br>
            <br>
            <h3><i>Select your book parameters!</i></h3>
        </div>
        <div v-else class="bookitem" @click="selectBook" v-for="book in stats.queriedBooks" v-bind:key="book.idx">
            <hr class="sub-breaker">
            <b>{{ book.title }}</b>
            <br>
            <i>{{ book.author }}</i>
        </div>
    </div>
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

export default {
    name: 'Stats',
    data() {
        return {
            sliderValue: null,
            sliderPosition: this.$store.getters.sliderPosition,
            queriedBooks: this.$store.getters.queriedBooks,
            clicked: false
        }
    },
    computed: {
        // TODO : fix these awful naming conventions. will inevitably come when sliderPosition is mapped to homunculus body parts
        stats() {
            return {
                sliderPosition: this.$store.getters.sliderPosition,
                queriedBooks: this.$store.getters.queriedBooks,
                clicked: false
            }
        },
    },
    methods: {
        selectBook: function(event){
            console.log("click!")
            // stats.clicked = !stats.clicked
            // console.log(stats.clicked)
            console.log(event)
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
    h2 { 
        color: white
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
    .defaultstats{
        opacity: 0.4    ;
    }
    .bookitem{
        color: white
    }
    .bookscontainer{
        overflow-y: auto;
        height: 15vmax;
    }
    .slidecontainer {
        width: 20vmax;
        background: #cccccc;
        background: linear-gradient( rgba(0, 0, 0, 0.25) 100%, #436f7c 100%),
  url('/static/bg.jpg') no-repeat center center fixed;
    }
</style>