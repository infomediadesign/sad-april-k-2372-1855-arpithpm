<template>
    <div class="container">
        <div class="row">
            <div class="col-md-4"></div>
            <div class="col-md-4">
                <b-toast id="example-toast" no-close-button class="mt-5" variant="success" title="SignUp" static
                         no-auto-hide>
                    Email Verification Successful. Thank You.
                </b-toast>
                <b-overlay :show="isloading" rounded="sm">
                    <b-card class="mt-3" header="Email Verification" v-if="!done">
                        <!--                    Here we show the error messages-->
                        <b-alert v-model="errors" variant="danger" dismissible v-if="errors">
                            <ul class="mx-0 px-0" v-for="(key, ind) in err_messages" :key="ind">
                                <p class="my-0"><strong>{{titleizes(ind)}}</strong></p>
                                <span v-for="(val, ind) in key" :key="ind">{{val}}</span>
                            </ul>
                        </b-alert>
                    </b-card>
                </b-overlay>
            </div>
        </div>

    </div>
</template>

<script>
    import axios from "axios";
    import {emailverification} from "@/urls";
    const titleize = require('titleize');


    export default {
        data() {
            return {
                key:"",
                isloading: false,
                errors: false,
                err_messages: [],
                done: false
            }
        },
        mounted(){
            this.key = this.$route.params.key;
            this.onSubmit()
        },

        methods: {
            titleizes: val => titleize(val),
            onSubmit: function () {
                this.isloading = true;
                axios.post(emailverification, {key: this.key})
                    .then((resp) => {
                        console.log(resp.data);
                        this.isloading = false;
                        this.done = true;
                        this.$bvToast.show('example-toast')
                    })
                    .catch((err) => {
                        this.isloading = false;
                        this.errors = true;
                        if (!err.status) {
                            this.err_messages = {"Network Error" : "Please check your Internet Connection."};
                            return
                        }
                        console.log(err.response.data);
                        this.err_messages = err.response.data;
                    })
            },
            onReset() {
                this.errors = false;
                this.isloading = false;
                this.err_messages = [];
                this.key = "";
                this.password = "";
                this.done = false

            },

        }
    }
</script>