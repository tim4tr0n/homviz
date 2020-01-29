<template>
  <div class="slidecontainer">
    <h3>Homunculus Stats</h3>
    <hr>
    <p><u>sampled works</u>: <i>({{stats.queriedBooks.length}} books queried)</i></p>
    <div class="bookscontainer">
        <div v-if="stats.queriedBooks.length == 0" class="defaultstats">
            <br>
            <br>
            <h3><i>Select your book parameters!</i></h3>
        </div>
        <div v-else v-bind:class="{ selected: book == stats.selectedBook, bookitem: !(book == stats.selectedBook) }" v-for="(book, index) in stats.queriedBooks" @click="selectBook(book, index)" v-bind:key="book.idx">
            <hr class="sub-breaker">
            <b>{{ book.title }}</b>
            <br>
            <i>{{ formatAuthor(book.author) }}</i>
        </div>
    </div>
    <hr class="sub-breaker">
    <p><u>year range</u></p>
    <h4><b>1840</b> - <b>1920</b></h4>
    <hr class="sub-breaker">
    <p><u>body_state</u></p>
    <div class="bodypartscontainer">
        <div v-if="stats.bodyState == null" class="defaultstats">
           
            <h3><i>Select a book!</i></h3>
        </div>
        <div v-else-if="stats.selectedBook != null && Object.keys(stats.bodyState).length == 0" class="defaultstats">
            <br>
            <br>
            <h3><i>No bodyparts  are mentioned! What a sorry excuse for a book.</i></h3>
        </div>
        <div v-else class="bodypartitem" v-for="(value, key) in stats.bodyState" v-bind:key="key">
            <b>{{key}}</b> : <i>{{value}}</i>
        </div>
    </div>
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
            bodyState: this.$store.getters.bodyState,
            bodyParts: this.$store.getters.bodyParts,
            selectedBook: this.$store.getters.selectedBook
        }
    },
    computed: {
        // TODO : fix these awful naming conventions. will inevitably come when sliderPosition is mapped to homunculus body parts
        stats() {
            return {
                sliderPosition: this.$store.getters.sliderPosition,
                bodyState: this.$store.getters.bodyState,
                queriedBooks: this.$store.getters.queriedBooks,
                selectedBook: this.$store.getters.selectedBook,
                bodyParts: this.$store.getters.bodyParts
            }
        },
        bookBodyParts() {
            const selectedBook = this.$store.getters.selectedBook;
            const bodyParts  = this.$store.getters.bodyParts;
            const bookBodyParts = Object.keys(selectedBook) // this name is not the best. we're getting the keys of the selected book object that are body parts
                .filter(key => key in bodyParts)
                .reduce((obj, key) => {
                    return {
                        ...obj,
                        [key]: selectedBook[key]
                    };
                }, {});
            return bookBodyParts
            
        }
    },
    methods: {
        selectBook: function(book, index){
            console.log(book, index)
            this.$store.dispatch('changeSelectedBookAndBodyState', { book, index } )
        },
        formatAuthor(author){
            if(author == null){
                return author
            }
            if(author.includes(", ")){
                const split = author.split(", ")
                return split[1] + " " + split[0]
            }
            return author
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .sub-breaker {
        opacity: 0.1;
        margin-top: 0px;
        margin-bottom: 15px;
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
        opacity: 0.4;
        text-align: center;
    }
    .selected{
        background: #4f518c;
        color: white;
        padding-bottom:10px;
    }
    .bookitem{
        color: white;
        padding-bottom:10px;
    }
    .bookscontainer{
        overflow-y: auto;
        height: 15vmax;
        text-align: center;
    }
    .bodypartscontainer{
        overflow-y: auto;
        height: 8vmax;
        margin: 15px;
    }
    .bodypartitem{
        color: white;
        margins: 15px;
    }
    .slidecontainer {
        width: 20vmax;
        background: #cccccc;
        background: linear-gradient( rgba(0, 0, 0, 0.25) 100%, #436f7c 100%),
  url('/static/bg.jpg') no-repeat center center fixed;
    }
</style>