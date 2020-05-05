<template>
    <div class="container mt-2">
        <!--        <div class="col-md-6">-->
        <!--            <Errormessage v-if="errorobj" :errorobj="errorobj"></Errormessage>-->
        <!--        </div>-->
        <div class="row">
            <div class="col-md-10">
                <div class="row">
                    <div class="col">
                        <h4>My Pets</h4>
                    </div>
                    <div class="col text-right">
                        <b-button variant="primary" :to="{name: 'addnewpet'}">+ Add New Pet</b-button>
                    </div>
                </div>
                <hr class="">

            </div>
        </div>
        <div class="row">
            <div class="col-md-4">
                <Errormessage v-if="errorobj" :errorobj="errorobj"></Errormessage>
                <div v-if="pets.length < 1 && pets !== undefined">
                    <b-alert :show="pets.length < 1 || pets === undefined" variant="danger">No Pets found. Add a new
                        Pet.
                    </b-alert>
                    <hr>
                </div>
            </div>
        </div>
        <b-overlay :show="loading" rounded="sm">
            <div class="row">
                <div class="col-md-5 pr-0" v-for="(pet,ind) in pets" :key="ind">
                    <b-card :header="titlize(pet.name)" class="my-1" border-variant="secondary">
                        <b-list-group>
                            <b-list-group-item class="flex-column align-items-start">
                                <div class="d-flex w-100 justify-content-between">
                                    <h5 class="mb-1">{{pet.name}}</h5>
                                    <small>{{pet.breedobj.category.name}} |
                                        {{getAgeOfPet(pet.date_of_birth)}}</small>
                                </div>
                                <hr class="my-2">
                                <div class="row">
                                    <div class="col">
                                        <p>Breed: {{pet.breedobj.name}}
                                        </p>
                                    </div>
                                    <div class="col">
                                        <p>Plan: {{pet.breedobj.plan.name}}
                                        </p>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col">
                                        <strong>Instructions:</strong> {{pet.instructions}}
                                    </div>
                                </div>
                                <hr class="my-2">
                                <div class="row">
                                    <div class="col">
                                        <b-button size="sm" variant="danger" @click="deletePet(pet.id)">Delete Pet
                                        </b-button>
                                    </div>
                                </div>
                            </b-list-group-item>
                        </b-list-group>
                    </b-card>
                </div>
            </div>
        </b-overlay>


    </div>

</template>

<script>
    import moment from "moment";

    const titleize = require('titleize');
    import axios from "axios";
    import {userpets} from "@/urls";
    import Errormessage from "@/components/Utilities/Errormessage";

    const DateDiff = require('date-diff');

    export default {
        data() {
            return {
                pets: undefined,
                // to display errormessage component
                errorobj: undefined,
                loading: false
            }
        },
        props: {},
        methods: {
            getUserPets() {
                this.errorobj = undefined;
                this.loading = true
                axios.get(userpets)
                    .then(res => {
                        this.pets = res.data
                    }).catch(err => {
                    if (err.response) {
                        /*
                         * The request was made and the server responded with a
                         * status code that falls out of the range of 2xx
                         */
                        // console.log("* The request was made and the server responded with a status code that falls out of the range of 2xx");
                        // console.log(err.response.data);
                        this.errorobj = err.response.data
                        // console.log(err.response.status);
                        // console.log(err.response.headers);
                    } else if (err.request) {
                        /*
                         * The request was made but no response was received, `err.request`
                         * is an instance of XMLHttpRequest in the browser and an instance
                         * of http.ClientRequest in Node.js
                         */
                        this.errors = true;
                        this.errorobj = {"message": "Oops! No Response was received from the Server, Sorry."};
                    }
                }).then(() => {
                    this.loading = false
                })
            },
            titlize(pet) {
                return titleize(pet)
            },
            getAgeOfPet(dob) {
                let birth = moment(dob, "YYYY-MM-DD").toDate();
                let cur_date = moment(new Date(), "yyyy-mm-dd",).toDate();
                let diff = new DateDiff(cur_date, birth);
                if (diff.years() == 0) {
                    return " <1 year old"
                }
                return diff.years() + " years old"

            },
            deletePet(val) {
                this.$bvModal.msgBoxConfirm('Are you sure you want to delete the Pet details?', {
                    okVariant: 'danger',
                })
                    .then(value => {
                        if (value) {
                            this.loading = true
                            axios.delete(userpets + val + "/")
                                .then(res => {
                                    if (res.status === 204) {
                                        this.$bvModal.msgBoxOk('Pet Details Deleted.')
                                            .then(() => {
                                                this.getUserPets()
                                            })
                                    }
                                }).catch(err => {
                                if (err.response) {
                                    /*
                                     * The request was made and the server responded with a
                                     * status code that falls out of the range of 2xx
                                     */
                                    // console.log("* The request was made and the server responded with a status code that falls out of the range of 2xx");
                                    // console.log(err.response.data);
                                    // console.log(err.response.status);
                                    // console.log(err.response.headers);
                                    this.errorobj = err.response.data

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
                            }).then(() => {
                                this.loading = true
                            })
                        }
                    })
                // .catch(err => {
                //     // An error occurred
                // })
            }
        },

        created() {
            this.getUserPets()
        },
        components: {
            Errormessage
        },
    };
</script>
