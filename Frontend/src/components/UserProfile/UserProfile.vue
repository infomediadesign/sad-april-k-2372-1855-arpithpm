<template>
    <div class="col-md-12">
        <h4>User Profile</h4>
        <hr>
        <div class="row justify-content-center">
            <div class="col-md-4">
                <Errormessage v-if="errorobj" :errorobj="errorobj"></Errormessage>
                <b-overlay :show="!userobj || loading" rounded="sm">
                    <b-card header="Profile Details">
                        <b-form @submit="onSubmit">
                            <div class="row">
                                <div class="col">
                                    <b-form-group
                                            id="input-group-1"
                                            label="Email address:"
                                            label-for="input-1"
                                            description="Email cannot be changed at this moment.">
                                        <b-form-input
                                                id="input-1"
                                                disabled
                                                v-model="userobj.email"
                                                type="email"
                                                placeholder="Enter email"
                                        ></b-form-input>
                                    </b-form-group>
                                </div>
                            </div>
                            <div>
                                <b-form-group id="input-group-2" label="First Name:" label-for="input-2">
                                    <b-form-input
                                            id="input-2"
                                            v-model="form.first_name"
                                            required
                                            placeholder="Type you First Name."
                                    ></b-form-input>
                                </b-form-group>

                                <b-form-group id="input-group-3" label="First Name:" label-for="input-3">
                                    <b-form-input
                                            id="input-3"
                                            v-model="form.last_name"
                                            required
                                            placeholder="Type you Last Name."
                                    ></b-form-input>
                                </b-form-group>


                                <b-button type="submit" :disabled="!showSubmitbtn" variant="primary" class="mx-1">Update
                                </b-button>
                            </div>
                        </b-form>
                    </b-card>
                </b-overlay>
            </div>
        </div>

    </div>
</template>

<script>
    import {userprofile} from "@/urls";

    import axios from "axios";
    import Errormessage from "@/components/Utilities/Errormessage";

    export default {
        props: {},
        data() {
            return {
                form: {
                    first_name: "",
                    last_name: "",
                },


                userobj: undefined,
                errorobj: false,
                // for toggling submit btn. Show only if data is changed.
                showSubmitbtn: false,
                // for loading overlay
                loading: false
            }
        },
        created() {
            axios.get(userprofile)
                .then(res => {
                    this.userobj = res.data;
                    this.form.first_name = res.data.first_name;
                    this.form.last_name = res.data.last_name
                })
                .catch(err => {
                    if (err.response) {
                        /*
                         * The request was made and the server responded with a
                         * status code that falls out of the range of 2xx
                         */
                        // console.log("* The request was made and the server responded with a status code that falls out of the range of 2xx");
                        // console.log(err.response.data);
                        // console.log(err.response.status);
                        // console.log(err.response.headers);
                    } else if (err.request) {
                        /*
                         * The request was made but no response was received, `err.request`
                         * is an instance of XMLHttpRequest in the browser and an instance
                         * of http.ClientRequest in Node.js
                         */
                        this.errorobj = {"message": "Oops! No Response was received from the Server, Sorry."};
                        // console.log("The request was made but no response was received, `err.request` is an instance of XMLHttpRequest in the browser and an instance of http.ClientRequest in Node.js");
                        // console.log(err.request);
                    }
                })
        },
        methods: {

            onSubmit(event) {
                event.preventDefault();
                this.errorobj = false;
                this.loading = true;
                axios.put(userprofile, {...this.form})
                    .then(res => {
                        this.userobj = {...res.data};
                        this.form = {...res.data};
                        this.$store.commit("setUsernameOnProfileUpdate", res.data.first_name);
                        this.$bvModal.msgBoxOk('Profile Updated!')

                        // this.showSubmitbtn = false
                    })

                    .catch(err => {
                        if (err.response) {
                            /*
                             * The request was made and the server responded with a
                             * status code that falls out of the range of 2xx
                             */
                            // console.log("* The request was made and the server responded with a status code that falls out of the range of 2xx");
                            // console.log(err.response.data);
                            // console.log(err.response.status);
                            // console.log(err.response.headers);
                        } else if (err.request) {
                            /*
                             * The request was made but no response was received, `err.request`
                             * is an instance of XMLHttpRequest in the browser and an instance
                             * of http.ClientRequest in Node.js
                             */
                            this.errorobj = {"message": "Oops! No Response was received from the Server, Sorry."};
                            // console.log("The request was made but no response was received, `err.request` is an instance of XMLHttpRequest in the browser and an instance of http.ClientRequest in Node.js");
                            // console.log(err.request);
                        }
                    }).finally(() => {
                    this.loading = false;

                })
            }
        },
        watch: {
            form: {
                deep: true,
                handler: function (val) {
                    this.showSubmitbtn = !(val.first_name === this.userobj.first_name && val.last_name === this.userobj.last_name);
                }
            }
        },
        components: {
            Errormessage: Errormessage

        }
    };
</script>
