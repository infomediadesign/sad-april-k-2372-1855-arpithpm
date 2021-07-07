<template>
    <div class="container">
        <div class="row">
            <div class="col-md-4"></div>
            <div class="col-md-4">
                <b-toast id="example-toast" no-close-button class="mt-5" variant="success" title="SignUp" static
                         no-auto-hide>
                    Password reset link has been sent to your email.
                </b-toast>
                <b-overlay :show="isloading" rounded="sm">
                    <b-card class="mt-3" header="Reset Password" v-if="!done">
                        <!--                    Here we show the error messages-->
                        <b-alert v-model="errors" variant="danger" dismissible v-if="errors">
                            <ul class="mx-0 px-0" v-for="(key, ind) in err_messages" :key="ind">
                                <p class="my-0"><strong>{{titleizes(ind)}}</strong></p>
                                <span v-for="(val, ind) in key" :key="ind">{{val}}</span>
                            </ul>
                        </b-alert>
                        <!--                        end of error messages-->
                        <b-form @submit="onSubmit" @reset="onReset">
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
                            <hr class=" my-1">
                            <p class="my-1">Don't have an account?
                                <router-link to="signup" exact>Sign Up</router-link>
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
    import axios from "axios";
    import {resetpassword} from "@/urls";
    const titleize = require('titleize');


    export default {
        data() {
            return {
                password: "",
                key:"",
                isloading: false,
                errors: false,
                err_messages: [],
                done: false
            }
        },
        mounted(){
            this.key = this.$route.params.key
        },

        methods: {
            titleizes: val => titleize(val),
            onSubmit(evt) {
                evt.preventDefault();
                this.isloading = true;
                axios.post(resetpassword, {key: this.key, password: this.password})
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