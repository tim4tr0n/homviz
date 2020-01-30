<template>
  <div class="slidecontainer">
    <hsc-window-style-metal>
        <hsc-window title="hom info" >
            <fieldset>
                <legend>pointy pointy</legend>
                {{ selectorData.sliderPosition }}
            </fieldset>
            <fieldset>
                <legend>Genre</legend>
                <select @input="updateGenre">
                    <option value="none" selected>Choose a genre</Option>
                    <option v-for="(value, key) in selectorData.genres"  v-bind:key="key" v-bind:value="key">{{value}}</option>
                </select>
            </fieldset>
            <fieldset>
                <legend>Subgenre</legend>
                <select @input="updateSubgenre">
                    <option value="none" selected>All</Option>
                    <option v-for="(value, key) in selectorData.subgenres"  v-bind:key="key" v-bind:value="key">{{value}}</option>
                </select>
            </fieldset>
            <fieldset>
                <legend>Language</legend>
                <select @input="updateLanguage">
                    <option value="none" selected>Choose a language</Option>
                    <option v-for="(value, key) in selectorData.languages"  v-bind:key="key" v-bind:value="key">{{value}}</option>
                </select>
            </fieldset>
            <fieldset>
                <legend>thigh</legend>
                <input @input="($event) => { updateHomunculusPart( $event, 'thigh' ) }" type="range" />
            </fieldset>
            <fieldset>
                <legend>neck</legend>
                <input @input="($event) => { updateHomunculusPart( $event, 'neck' ) }" type="range" />
            </fieldset>
            <fieldset>
                <legend>penile gratuity</legend>
                <input type="radio" name="gender" value="male">fuck yea
                <br>
                <input type="radio" name="gender" value="female">hell no
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
            sliderPosition: this.$store.getters.sliderPosition,
            genres: this.$store.getters.genres,
            subgenres: this.$store.getters.subgenres,
            languages: this.$store.getters.languages,
            selectedGenre: this.$store.getters.selectedGenre,
            selectedSubgenre: this.$store.getters.selectedSubgenre,
            selectedLanguage: this.$store.getters.selectedLanguage
        }
    },
    methods: {
        updateGenre(e) {
            this.$store.commit("changeSelectedGenre", e.srcElement.value)
        },
        updateSubgenre(e) {
            this.$store.commit("changeSelectedSubgenre", e.srcElement.value)
        },
        updateLanguage(e) {
            this.$store.commit("changeSelectedLanguage", e.srcElement.value)
        },
        updateHomunculusPart(e, part) {
            this.$store.commit("changeHomunculusPartState", { sliderValue: e.srcElement.valueAsNumber, part } )
        }
    },
    computed: {
        // TODO : fix these awful naming conventions. will inevitably come when sliderPosition is mapped to homunculus body parts
        selectorData() {
            return {
                sliderPosition: this.$store.getters.sliderPosition,
                genres: this.$store.getters.genres,
                subgenres: this.$store.getters.subgenres,
                languages: this.$store.getters.languages,
                selectedLanguage: this.$store.getters.selectedLanguage,
                homunculusState: this.$store.getters.homunculusState
            }
        },
   
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    select {
        width: 100%
    }
</style>