<template>
    <b-alert variant="danger" dismissible show>
        <ul class="mx-0 px-0 mb-0" v-for="(key, ind) in errorobj" :key="ind">
            <p class="my-0"><strong>{{titleizes(ind)}}</strong></p>
            <span v-for="(val, ind) in key" :key="ind">{{val}}</span>
        </ul>
    </b-alert>
</template>
<script>
    const titleize = require('titleize');
    export default {
        props: {"errorobj": Object},
        methods: {
            titleizes: val => titleize(val),

        }
    }
</script>

<style>

</style>