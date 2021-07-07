<template>
    <b-container class="mt-2">
        <div class="row">
            <div class="col-sm-12 col-md-8">
                <h4>My Bookings</h4>
                <hr class="">
                <b-col sm="12" md="12">
                    <b-overlay :show="loading" spinner-variant="primary" rounded="sm">
                        <b-row>
                            <b-col v-for="(val, ind) in userbookings" :key="ind" md="6">
                                <BookingCard :booking="val" class="my-1">
                                </BookingCard>
                            </b-col>
                        </b-row>
                    </b-overlay>
                    <b-row class="d-flex justify-content-center">
                        <b-alert show variant="danger" v-if="!dataexists" class="mx-3 text-center">No previous bookings.
                        </b-alert>
                    </b-row>
                </b-col>

            </div>
            <div class="col-sm-12 col-md-3">
                <b-card class="my-2"
                        header="Weekend Getaways?"
                        header-tag="header"
                >
                    <b-card-text>We're here to take good care of your pet. Book a stay for your pet now.</b-card-text>
                    <b-button :to="{name: 'booknow'}" variant="primary">Book Now</b-button>
                </b-card>
            </div>
        </div>
        <!--        <b-col sm="12" md="8">-->
        <!--            <b-row>-->
        <!--                <b-col v-for="(val, ind) in userbookings" :key="ind">-->
        <!--                    <BookingCard :booking="val" :pets="userpets" :paymentmethods="paymentmethods">-->
        <!--                    </BookingCard>-->
        <!--                </b-col>-->
        <!--            </b-row>-->
        <!--            <b-row class="d-flex justify-content-center">-->
        <!--                <b-alert show variant="danger" v-if="!dataexists" class="mx-3 text-center">No previous bookings.-->
        <!--                </b-alert>-->
        <!--            </b-row>-->
        <!--        </b-col>-->

    </b-container>
</template>

<script>
    import BookingCard from "../BookingCard/BookingCard"
    import axios from "axios";
    import {pastbookings} from "@/urls";

    export default {
        data() {
            return {
                loading: true,
                userbookings: {},
                dataexists: true
            }
        },
        methods: {
            paymentmethod(val) {
                let items;
                items = this.paymentmethods.filter(item => {
                    return item.id === val
                });
                return items[0].name
            }
        },
        components: {
            BookingCard: BookingCard,
        },
        beforeCreate() {

            axios.get(pastbookings)
                .then(resp => {
                    console.log(resp.data);
                    this.userbookings = resp.data;
                    this.loading = false;
                    if (resp.data.length === 0) {
                        this.dataexists = false
                    }
                })
                .catch(err => {
                    this.loading = false;
                    if (err.response) {
                        this.$bvToast.toast(err.response.data)
                    }
                })

        },
        created() {

        }
    }
</script>