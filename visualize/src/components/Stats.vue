<template>
  <div class="slidecontainer">
    <hsc-window-style-metal>
        <hsc-window title="hom info" >
            <fieldset>
                <legend>point pointy</legend>
                {{ slider.sliderPosition }}
            </fieldset>
            <fieldset>
                <legend>elasticity</legend>
                <input type="range" />
            </fieldset>
            <fieldset>
                <legend>penile gratuity</legend>
                <input type="radio" name="gender" value="male">fuck yea
                <br>
                <input type="radio" name="gender" value="female">hell no
            </fieldset>
            <fieldset>
                <legend>&beta;</legend>
                <input type="range" />
            </fieldset>
            <fieldset>
                <legend>&gamma;</legend>
                <input type="range" />
            </fieldset>
            <fieldset>
                <legend>search</legend>
                <input type="search" />
            </fieldset>
        </hsc-window>
    </hsc-window-style-metal>
    <!-- <ul>
        <li v-for="book in books.slice(0,2)" v-bind:key="book.idx">
        {{ book.title }} 
        </li> -->
    <!-- </ul> -->

  </div>
</template>

<script>
import Vue from 'vue'
import * as VueWindow from '@hscmap/vue-window'

Vue.use(VueWindow)
// import { db } from '../firebaseConfig';
export default {
    name: 'Stats',
    data() {
        return {
            sliderValue: null,
            books: [],
            sliderPosition: this.$store.getters.sliderPosition
        }
    },
    // firestore() {
    //     return {
    //         books: db.collection('books'),
    //     }
    // },

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
    /* .slidecontainer {
        width: 20vmax;
        height: 35vmax;
        background: #cccccc;
    } */
</style>