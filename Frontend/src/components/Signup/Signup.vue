<template>
    <div class="container">
        <div class="row">
            <div class="col-md-4"></div>
            <div class="col-md-4">
                <b-toast id="example-toast" no-close-button class="mt-5" variant="success" title="SignUp" static
                         no-auto-hide>
                    Please verify your email to signin.
                </b-toast>
                <b-overlay :show="isloading" rounded="sm">
                    <b-card class="mt-3" header="Sign Up" v-if="!done">
                        <!--                    Here we show the error messages-->
                        <b-alert v-model="errors" variant="danger" dismissible>
                            <ul class="mx-0 px-0 mb-0" v-for="(key, ind) in err_messages" :key="ind">
                                <p class="my-0"><strong>{{titleizes(ind)}}</strong></p>
                                <span v-for="(val, ind) in key" :key="ind">{{val}}</span>
                            </ul>
                        </b-alert>
                        <!--                        end of error messages-->
                        <b-form @submit="onSubmit" @reset="onReset">
                            <b-form-group id="input-group-2" label="Your Name:" label-for="input-2">
                                <b-form-input
                                        id="input-2"
                                        v-model="name"
                                        required
                                        placeholder="Enter name"
                                />
                            </b-form-group>
                            <b-form-group
                                    id="input-group-1"
                                    label="Email address:"
                                    label-for="input-1"
                                    description="We'll never share your email with anyone else."
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
                                    description="Enter a super strong password."
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
                            <hr class="">
                            <p class="my-1">Already have an account?
                                <router-link :to="{name: 'signin'}" exact>Log In</router-link>
                            </p>
                        </b-form>
                        <!--                        <b-card class="mt-3" header="Form Data Result">-->
                        <!--                            <pre class="m-0">{{ form }}</pre>-->
                        <!--                        </b-card>-->
                    </b-card>
                </b-overlay>
            </div>
        </div>

    </div>
</template>

<script>
    import {signup} from "../../urls"
    import axios from "axios";

    const titleize = require('titleize');

    export default {
        data() {
            return {
                email: '',
                name: '',
                password: "",
                isloading: false,
                done: false,
                errors: false,
                err_messages: undefined
            }
        },
        watch: {
            name: function () {
                this.name = titleize(this.name)
            }
        },
        methods: {
            initstate() {
                this.isloading = false;
                this.done = false;
                this.errors = false;
                this.err_messages = {}
            },
            titleizes: val => titleize(val),

            onSubmit(evt) {
                evt.preventDefault();
                this.initstate();
                this.isloading = true;
                axios.post(signup, {
                    first_name: titleize(this.name),
                    email: this.email,
                    password: this.password
                })
                    .then(resp => {
                        console.log(resp.data);
                        this.isloading = false;
                        this.done = true;
                        this.$bvToast.show('example-toast')
                    })
                    .catch((err) => {
                        this.isloading = false;
                        this.errors = true;
                        if (err.response) {
                            console.log(err.response.data);
                            this.err_messages = err.response.data;
                        } else if (err.request) {
                            // this.err_messages = {"Network Error": "Please check your Internet Connection."};
                            this.err_messages = {"Network Error": "Please check your Internet Connection."};
                        } else {
                            // this.err_messages = {"Network Error": "Please check your Internet Connection."};
                            this.err_messages = {"Network Error": "Please check your Internet Connection."};
                        }

                    })
            },
            onReset(evt) {
                evt.preventDefault();
                // Reset our form values
                this.email = '';
                this.name = '';
                this.password = '';
                this.initstate()

            }
        }
    }
</script>