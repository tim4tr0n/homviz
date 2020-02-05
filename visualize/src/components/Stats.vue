<template>
  <div class="slidecontainer">
    <h3>Homunculus Stats</h3>
    <hr>
    <p><u>sampled works</u>: <i>({{stats.queriedBooks.length}} books queried)</i></p>
    <div class="bookscontainer" id="bookscontainer">
        <div v-if="stats.queriedBooks.length == 0" class="defaultstats">
            <br>
            <loading :active.sync="stats.loadingBooks"
            :can-cancel="false" 
            :is-full-page="false"></loading>
            <br>
            <h3><i>No books queried. Change your book parameters!</i></h3>
        </div>
        <div v-else v-bind:id="'index' + index" v-bind:class="{ selected: book == stats.selectedBook, bookitem: !(book == stats.selectedBook) }" v-for="(book, index) in stats.queriedBooks" @click="selectBook(book, index)" v-bind:key="book.idx">
            <div>
                <hr class="sub-breaker">
                <b>{{ book.title }}</b>
                <br>
                <i>{{ formatAuthor(book.author) }}</i>
            </div>
        </div>
    </div>
    <div v-if="stats.viewByYearMode">
        <hr class="sub-breaker">
        <p><u>year range</u> <b>{{ stats.earliestYear }} - {{ stats.latestYear }}</b></p>

        <div v-if="stats.selectedBook"> <p><u>selected year</u>  <b>{{ stats.selectedBook.publicationDate }} </b>  </p> </div>
    </div>
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
import Loading from 'vue-loading-overlay';
import anime from 'animejs'; // https://github.com/juliangarnier/anime
// import VueScrollTo from 'vue-scrollto';
// Import stylesheet
import 'vue-loading-overlay/dist/vue-loading.css';

Vue.use(VueWindow)
// Vue.use(VueScrollTo)

export default {
    name: 'Stats',
    data() {
        return {
            sliderValue: null,
            sliderPosition: this.$store.getters.sliderPosition,
            queriedBooks: this.$store.getters.queriedBooks,
            bodyState: this.$store.getters.bodyState,
            bodyParts: this.$store.getters.bodyParts,
            selectedBook: this.$store.getters.selectedBook,
            isLoading: true,
            loadingBooks: this.$store.getters.loadingBooks,
            viewByYearMode: this.$store.getters.viewByYearMode
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
                bodyParts: this.$store.getters.bodyParts,
                loadingBooks: this.$store.getters.loadingBooks,
                earliestYear: this.$store.getters.earliestYear,
                latestYear: this.$store.getters.latestYear,
                viewByYearMode: this.$store.getters.viewByYearMode
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
    mounted: function() {
        // var options = {
        //     container: '#bookscontainer',
        //     easing: 'ease-in',
        //     offset: -60,
        //     force: true,
        //     cancelable: true,
        //     // onStart: function(element) {
        //     // // scrolling started
        //     // },
        //     // onDone: function(element) {
        //     // // scrolling is done
        //     // },
        //     // onCancel: function() {
        //     // // scrolling has been interrupted
        //     // },
        //     // x: false,
        //     // y: true
        // }

        this.$store.subscribe((mutation) => {
            if( mutation.type == "changeSelectedBookIndex"){
                console.log("attempting to scroll")
                // var id = mutation.payload
                this.scroll({ 
                    to: ".selected"
                });
                // var cancelScroll = VueScrollTo.scrollTo(id, 300, options)
                // cancelScroll()
            }
        });


    },
    components: {
        Loading
    },
    methods: {
        scroll(arg) {
            let el = document.querySelector(arg.to),
                offset = parseInt(arg.offset) || 0,
                duration = arg.duration || 800,
                easing = arg.easing || 'easeOutExpo',
                callback = arg.callback || null;
            console.log("el", el)
            if ( el ) {
                anime({
                    targets: ['#bookscontainer'],
                    scrollTop: (el.offsetTop - offset),
                    duration: duration,
                    easing: easing,
                    complete: callback
                })
                .finished.then(() => {
                    console.log("finished")
                    this.$emit('scroll:finished', true);
                });
            }
        },
        getId(book){
            if (book == this.stats.selectedBook){
                return "selectedBookId"
            }
            return "standardBookId"
        },
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
    #selectedBookId {
        
    }
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