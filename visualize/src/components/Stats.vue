<template>
  <div class="slidecontainer">
    <h1>Homunculus Info</h1>
    <p> <strong> spinny spinny: </strong> {{ slider.sliderPosition }} </p>
    <!-- <ul>
        <li v-for="book in books.slice(0,2)" v-bind:key="book.idx">
        {{ book.title }} 
        </li>
    </ul> -->
  </div>
</template>

<script>
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
    .slidecontainer {
        width: 20vmax;
        height: 35vmax;
        background: #cccccc;
    }
</style>