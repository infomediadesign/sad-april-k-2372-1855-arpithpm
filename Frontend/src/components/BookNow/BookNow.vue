<template>
    <div class="w-100">
        <div class="row">
            <div class="col">
                <h5 class="mx-4">Make a new Booking</h5>
                <hr>
            </div>
        </div>
        <b-overlay :show="requestloading" rounded="sm">
            <div class="row">
                <b-col md="6">
                    <Errormessage v-if="errorobj" :errorobj="errorobj"></Errormessage>
                    <b-row>
                        <b-col>
                            <b-overlay :show="isloading" rounded="sm">
                                <b-card header="Select your pet" :border-variant="selectedpet ? 'success': 'secondary'">
                                <b-alert :show="!pets.length" variant="danger" >No Pets found. <b-link :to="{name: 'addnewpet'}">Add a Pet</b-link> to make a Booking.</b-alert>
                                    <b-list-group>
                                        <b-list-group-item v-for="(val) in pets" href="#" :key="val.id"
                                                           :active="val.id === selectedpet" @click="setSelectedPet(val)"
                                                           class="flex-column align-items-start">
                                            <div class="d-flex w-100 justify-content-between">
                                                <h5 class="mb-1">{{val.name}}</h5>
                                                <small>{{val.breedobj.category.name}} |
                                                    {{getAgeOfPet(val.date_of_birth)}}</small>
                                            </div>
                                            <hr class="my-2">
                                            <div class="row">
                                                <div class="col">
                                                    <p>Breed: {{val.breedobj.name | capitalize}}
                                                    </p>
                                                </div>
                                                <div class="col">
                                                    <p>Plan: {{val.breedobj.plan.name}}
                                                    </p>
                                                </div>
                                            </div>
                                        </b-list-group-item>
                                    </b-list-group>
                                </b-card>
                            </b-overlay>
                        </b-col>
                        <!--                        <b-col>-->
                        <!--                        </b-col>-->
                    </b-row>
                    <div class="row mt-2">
                        <div class="col">
                            <b-card header="Payment Method"
                                    :border-variant="selectedpaymentmethod ? 'success': 'secondary'">
                                <b-list-group>
                                    <b-list-group-item v-for="(val, ind) in paymethods" :key="ind">
                                        <b-form-radio v-model="selectedpaymentmethod" name="some-radios"
                                                      :value="val.id">
                                            {{val.name}}
                                        </b-form-radio>
                                    </b-list-group-item>
                                </b-list-group>
                            </b-card>
                        </div>
                    </div>

                    <!--                    <a href="#" class="card-link">Card link</a>-->
                    <!--                    <b-link href="#" class="card-link">Another link</b-link>-->
                    <!--                </b-card>-->
                </b-col>
                <b-col md="6">
                    <b-card header="Check In/Out Dates"
                            :border-variant="selectedpet && numberOfDays ? 'success' : 'secondary'">
                        <!--                    <b-card-title class="mx-2">Check In/Out Dates:</b-card-title>-->
                        <b-row>
                            <b-col>
                                <v-date-picker
                                        mode="range"
                                        :value="null"
                                        color="blue"
                                        v-model="val"
                                        :min-date='new Date()'
                                        is-inline
                                />
                            </b-col>
                            <b-col>
                                <h6>Check-in: {{checkInforDisplay}}</h6>
                                <h6>Check-out: {{checkOutforDisplay}}</h6>
                                <h6>No. of Days: {{numberOfDays === undefined ? " - " : numberOfDays}}</h6>
                                <b-alert :show="showMinimumDayError" variant="danger">Minimum Booking Period: 1 Day
                                </b-alert>
                                <hr>
                                <h6 v-show="numberOfDays && selectedpet">Total Cost: {{price}} * {{numberOfDays}} =
                                    {{price
                                    * numberOfDays}}</h6>
                            </b-col>
                        </b-row>
                        <!--                    <b-card-text>-->
                        <!--                        Some quick example text to build on the <em>card title</em> and make up the bulk of the card's-->
                        <!--                        content.-->
                        <!--                    </b-card-text>-->

                        <!--                    <b-card-text>A second paragraph of text in the card.</b-card-text>-->

                        <!--                    <a href="#" class="card-link primary" >Confirm</a>-->
                        <div class="row my-3">
                            <div class="col" v-show="validateForBooking">
                                <b-button variant="primary" class="mr-1" @click="confirmbooking">Confirm
                                </b-button>
                                <b-button variant="danger" class="mx-1"
                                          @click="$router.push({name:'home'})">Cancel
                                </b-button>
                            </div>
                            <div class="col">
                            </div>
                        </div>
                        <!--                    <b-link href="#" class="card-link">Another link</b-link>-->
                    </b-card>
                </b-col>
            </div>
        </b-overlay>
    </div>
</template>

<script>
    import DatePicker from 'v-calendar/lib/components/date-picker.umd'
    import axios from "axios";
    import {userpets, paymentmethods, newbooking} from "@/urls";
    import moment from "moment";
    import Errormessage from "@/components/Utilities/Errormessage";

    const DateDiff = require('date-diff');
    const dateFormat = require('dateformat');
    export default {
        data() {
            return {
                val: {},
                isloading: true,
                checkindate: undefined,
                checkoutdate: undefined,
                numberOfDays: undefined,
                pets: [],
                paymethods: [],
                price: undefined,
                selectedpet: undefined,
                selectedpaymentmethod: undefined,
                errorobj: undefined,
                requestloading: false
            }
        },
        created() {

            axios.get(userpets)
                .then(resp => {
                    this.isloading = false;
                    this.pets = resp.data
                }).catch(error => {
                if (error.response) {
                    /*
                     * The request was made and the server responded with a
                     * status code that falls out of the range of 2xx
                     */
                    console.log("* The request was made and the server responded with a status code that falls out of the range of 2xx");
                    console.log(error.response.data);
                    console.log(error.response.status);
                    console.log(error.response.headers);
                } else if (error.request) {
                    /*
                     * The request was made but no response was received, `error.request`
                     * is an instance of XMLHttpRequest in the browser and an instance
                     * of http.ClientRequest in Node.js
                     */
                    console.log("The request was made but no response was received, `error.request` is an instance of XMLHttpRequest in the browser and an instance of http.ClientRequest in Node.js");
                    console.log(error.request);
                }
            });

            axios.get(paymentmethods)
                .then(resp => {
                    this.paymethods = resp.data
                })


        },
        computed: {
            showMinimumDayError() {
                let res;
                if (this.numberOfDays === undefined) {
                    res = false
                } else if (this.numberOfDays === 0) {
                    res = true
                }
                return res

            },
            checkInforDisplay() {

                if (this.checkindate) {
                    let chkin = this.checkindate.split("-");
                    return "  " + chkin[2] + "-" + chkin[1] + "-" + chkin[0]
                } else {
                    return " - "
                }
            },
            validateForBooking() {
                let res;
                if (this.numberOfDays === 0 || this.numberOfDays === undefined || this.selectedpaymentmethod === undefined || this.selectedpet === undefined) {
                    res = false
                } else {
                    res = true
                }
                // res = !(this.numberOfDays === 0 || this.selectedpet === undefined);
                return res
            },
            checkOutforDisplay() {
                if (this.checkoutdate) {
                    let chkin = this.checkoutdate.split("-");
                    return chkin[2] + "-" + chkin[1] + "-" + chkin[0]
                } else {
                    return " - "
                }
            }
        },
        watch: {
            val() {
                this.checkindate = dateFormat(this.val.start, "yyyy-mm-dd");
                this.checkoutdate = dateFormat(this.val.end, "yyyy-mm-dd");
                let diff = new DateDiff(this.val.end, this.val.start);
                this.numberOfDays = diff.days()
            }
        },
        props: {},
        methods: {
            confirmbooking() {
                this.requestloading = true;
                axios.post(newbooking, {
                    "check_in_date": this.checkindate,
                    "check_out_date": this.checkoutdate,
                    "userpet": this.selectedpet,
                    "paymentmethod": this.selectedpaymentmethod
                })
                    .then(() => {
                        this.$router.push({name: "bookingconfirmed"})
                    })
                    .catch(err => {
                        console.log(err);
                        this.errorobj = err.response.data;
                        this.requestloading = false
                    })
            },
            setSelectedPet(val) {
                this.selectedpet = val.id;
                this.price = val.breedobj.plan.price
            },

            getAgeOfPet(dob) {
                let birth = moment(dob, "YYYY-MM-DD").toDate();
                let cur_date = moment(new Date(), "yyyy-mm-dd",).toDate();
                let diff = new DateDiff(cur_date, birth);
                console.log(diff.years());
                if (diff.years() == 0){
                    return " <1 year old"
                }
                return diff.years() + " years old"

            }
        },
        filters: {
            capitalize: function (value) {
                if (!value) return '';
                value = value.toString();
                return value.charAt(0).toUpperCase() + value.slice(1)
            }
        },

        components: {
            "v-date-picker": DatePicker,
            Errormessage
        }
    };
</script>
