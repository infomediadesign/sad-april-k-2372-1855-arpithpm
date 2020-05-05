<template>
    <div class="container">
        <div class="row">
            <div class="col-md-4"></div>
            <div class="col-md-4">
                <b-overlay :show="isloading" rounded="sm" spinner-variant="primary">
                    <b-card class="mt-3" header="Log In">
                        <!--                    Here we show the error messages-->
                        <b-alert v-model="errors" variant="danger" dismissible v-if="errors">
                            <ul class="mx-0 px-0 mb-0" v-for="(key, ind) in err_messages" :key="ind">
                                <p class="my-0"><strong>{{titleizes(ind)}}</strong></p>
                                <span v-for="(val, ind) in key" :key="ind">{{val}}</span>
                            </ul>
                        </b-alert>
                        <!--                        end of error messages-->
                        <b-form @submit="onSubmit" @reset="onReset">
                            <b-form-group
                                    id="input-group-1"
                                    label="Email address:"
                                    label-for="input-1"
                            >
                                <b-form-input
                                        id="input-1"
                                        v-model="email"
                                        type="email"
                                        required
                                        placeholder="Enter email"
                                />
                            </b-form-group>

                            <b-form-group
                                    id="input-group-3"
                                    label="Password:"
                                    label-for="input-3"
                                    description="Enter your password."
                            >
                                <b-form-input
                                        id="input-3"
                                        v-model="password"
                                        type="password"
                                        required
                                        placeholder="Enter password"
                                />
                            </b-form-group>


                            <b-button type="submit" variant="primary">Submit</b-button>
                            <b-button type="reset" variant="danger" class="ml-1">Reset</b-button>
                            <p class="my-2 ">
                                <router-link :to="{name: 'requestpasswordreset'}" exact>Forgot Password?</router-link>
                            </p>
                            <hr class=" my-1">
                            <p class="my-1">Don't have an account?
                                <router-link :to="{name: 'signup'}" exact>Sign Up</router-link>
                            </p>
                        </b-form>
                    </b-card>
                </b-overlay>
            </div>
        </div>

    </div>
</template>


<script>
    import axios from "axios";
    import {login} from "../../urls"

    const titleize = require('titleize');
    export default {
        data() {
            return {
                email: "dummy@email.com",
                password: "demouserD1@",
                isloading: false,
                errors: false,
                err_messages: {}
            }
        },

        methods: {
            titleizes: val => titleize(val),
            initstate() {
                this.errors = false;
                this.isloading = false;
                this.err_messages = {}
            },
            onReset(evt) {
                evt.preventDefault();
                // Reset our form values
                this.email = '';
                this.password = '';
                this.initstate()

            },
            async onSubmit(evt) {
                evt.preventDefault();
                this.initstate();
                this.isloading = true;
                await axios.post(login, {
                    email: this.email,
                    password: this.password
                })
                    .then(resp => {
                        this.isloading = false;
                        this.$store.commit("setUserOnLogin", resp.data);
                        this.$router.push({name: "home"})
                    })
                    .catch((err) => {
                        this.isloading = false;
                        this.errors = true;
                        console.log(err);
                        if (err.response) {
                            console.log(err.response.data);
                            this.err_messages = err.response.data;
                            // return
                        } else if (err.request) {
                            // this.err_messages = {"Network Error": "Please check your Internet Connection."};
                            this.err_messages = {"Network Error": "Please check your Internet Connection."};
                        } else {
                            // this.err_messages = {"Network Error": "Please check your Internet Connection."};
                            this.err_messages = {"Network Error": "Please check your Internet Connection."};
                        }
                    })
            },
        }
    }
</script>