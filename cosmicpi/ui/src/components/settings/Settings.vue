<template>
<div class="row">
    <Login v-if="!isLogged"></Login>
    <Wifi v-if="isLogged"></Wifi>
</div>
</template>

<script>
import Login from '../Login.vue'
import Wifi from './Wifi.vue'


export default {
    components: { Login, Wifi },
    name: 'Settings',
    computed: {
        isLogged() {
            return this.$store.getters.isLogged();
        },
    },
}
</script>