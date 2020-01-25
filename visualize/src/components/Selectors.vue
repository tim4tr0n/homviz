<template>
  <div class="slidecontainer">
    <hsc-window-style-metal>
        <hsc-window title="hom info" >
            <fieldset>
                <legend>pointy pointy</legend>
                {{ slider.sliderPosition }}
            </fieldset>
            <fieldset>
                <legend>Genre</legend>
                <select>
                    <option value="Russian shit">Russian shit</option>
                    <option value="saab">Saab</option>
                    <option value="opel">Opel</option>
                    <option value="audi">Audi</option>
                </select>
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
                <legend>search</legend>
                <input type="search" />
            </fieldset>
        </hsc-window>
    </hsc-window-style-metal>
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
            books: [],
            sliderPosition: this.$store.getters.sliderPosition
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
    select {
        width: 100%
    }
    /* .slidecontainer {
        width: 20vmax;
        height: 35vmax;
        bac kground: #cccccc;
    } */
</style>