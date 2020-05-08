<template>
    <div style="overflow-x: scroll;">
        <div class="m-2" style="overflow: auto">
            <h4>Payments (Admin Access Only)</h4>
            <div class="col-md-6">
                <Errormessage v-if="errorobj" :errorobj="errorobj"></Errormessage>
            </div>
            <hr class="">
        </div>
        <div class="mt-2" style="overflow: auto">
            <b-table :busy="busyFlag" striped :fields="fields" hover fixed bordered primary-key="booking_number"
                     :items="items" style="width: auto;white-space: nowrap">

                <template v-slot:cell(check_in_date)="data">
                    {{data.item.check_in_date | dateformatter}}
                </template>

                <template v-slot:cell(check_out_date)="data">
                    {{data.item.check_out_date | dateformatter}}
                </template>

                <template v-slot:cell(booked_on_date)="data">
                    {{data.item.booked_on_date | dateformatter}}
                </template>

                <template v-slot:cell(receive_payment)="data">
                    <b-button :disabled="busyFlag" variant="danger" size="sm" v-if="!data.item.payment_done"
                              @click="confirmPaymentReceipt(data.item)">Receive Payment
                    </b-button>
                    <b-button :disabled="busyFlag" variant="success" size="sm" v-else>PAID</b-button>
                </template>
            </b-table>
            <!--        modal to confirm receipt of payment-->
            <b-modal id="confirm-receive-payment" title="Receive Payment" @ok="ok"
                     @cancel="cancelops">
                <div v-if="user_booking_obj" class="container">
                    <div class="row">
                        <div class="col">
                            <h4>From: <strong>{{user_booking_obj.person_name}}</strong></h4><br>
                            <h4>Amount: <strong>{{user_booking_obj.amount}}</strong></h4>
                        </div>
                        <div class="col">
                            <!--                        <label for="input-small">Small:</label>-->
                            <b-form-input v-model.number="amount_received" type="number" id="input-small"
                                          placeholder="Amount Received"></b-form-input>
                            <h4 v-if="amount_received >= user_booking_obj.amount">Return Change: <strong>{{amount_received
                                -
                                user_booking_obj.amount}}</strong></h4><br>
                            <!--                        <h4>Amount: <strong>{{user_booking_obj.amount}}</strong></h4>-->
                        </div>
                    </div>
                </div>
            </b-modal>
            <b-modal id="amount-received-success-modal" title="Payment Update Status">
                <div class="container">
                    <div class="row justify-content-center" v-if="confirmPaymentPostRequest">
                        <div class="col">
                            <h2 class="text-success">Success</h2>
                        </div>
                        <div class="col">
                            <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px"
                                 width="64" height="64"
                                 viewBox="0 0 172 172"
                                 style=" fill:#000000;">
                                <g transform="">
                                    <g fill="none" fill-rule="nonzero" stroke="none" stroke-width="1"
                                       stroke-linecap="butt"
                                       stroke-linejoin="miter" stroke-miterlimit="10" stroke-dasharray=""
                                       stroke-dashoffset="0" font-family="none" font-size="none"
                                       style="mix-blend-mode: normal">
                                        <path d="M0,172v-172h172v172z" fill="none"></path>
                                        <g id="original-icon" fill="#2ecc71">
                                            <path d="M13.4375,10.75c-4.44067,0 -8.0625,3.62183 -8.0625,8.0625v112.875c0,4.44067 3.62183,8.0625 8.0625,8.0625h13.4375v13.4375c0,4.44067 3.62183,8.0625 8.0625,8.0625h123.625c4.44067,0 8.0625,-3.62183 8.0625,-8.0625v-112.875c0,-4.44067 -3.62183,-8.0625 -8.0625,-8.0625h-13.4375v-13.4375c0,-4.44067 -3.62183,-8.0625 -8.0625,-8.0625zM13.4375,16.125h123.625c1.48022,0 2.6875,1.20728 2.6875,2.6875v112.875c0,1.48022 -1.20728,2.6875 -2.6875,2.6875h-123.625c-1.48022,0 -2.6875,-1.20728 -2.6875,-2.6875v-112.875c0,-1.48022 1.20728,-2.6875 2.6875,-2.6875zM145.125,37.625h13.4375c1.48022,0 2.6875,1.20728 2.6875,2.6875v112.875c0,1.48022 -1.20728,2.6875 -2.6875,2.6875h-123.625c-1.48022,0 -2.6875,-1.20728 -2.6875,-2.6875v-13.4375h104.8125c4.44067,0 8.0625,-3.62183 8.0625,-8.0625zM110.1875,43c-0.68237,0 -1.37524,0.26245 -1.90015,0.78735l-46.47485,46.47485l-19.59985,-19.59985c-1.0498,-1.0498 -2.75049,-1.0498 -3.80029,0c-1.0498,1.0498 -1.0498,2.75049 0,3.80029l21.5,21.5c0.5249,0.5249 1.20728,0.78735 1.90015,0.78735c0.69287,0 1.37524,-0.26245 1.90015,-0.78735l48.375,-48.375c1.0498,-1.0498 1.0498,-2.75049 0,-3.80029c-0.5249,-0.5249 -1.21777,-0.78735 -1.90015,-0.78735zM21.5,118.25c-1.48022,0 -2.6875,1.20728 -2.6875,2.6875v5.375c0,1.48022 1.20728,2.6875 2.6875,2.6875c1.48022,0 2.6875,-1.20728 2.6875,-2.6875v-5.375c0,-1.48022 -1.20728,-2.6875 -2.6875,-2.6875zM34.9375,118.25c-1.48022,0 -2.6875,1.20728 -2.6875,2.6875v5.375c0,1.48022 1.20728,2.6875 2.6875,2.6875c1.48022,0 2.6875,-1.20728 2.6875,-2.6875v-5.375c0,-1.48022 -1.20728,-2.6875 -2.6875,-2.6875zM48.375,118.25c-1.48022,0 -2.6875,1.20728 -2.6875,2.6875v5.375c0,1.48022 1.20728,2.6875 2.6875,2.6875c1.48022,0 2.6875,-1.20728 2.6875,-2.6875v-5.375c0,-1.48022 -1.20728,-2.6875 -2.6875,-2.6875zM61.8125,118.25c-1.48022,0 -2.6875,1.20728 -2.6875,2.6875v5.375c0,1.48022 1.20728,2.6875 2.6875,2.6875c1.48022,0 2.6875,-1.20728 2.6875,-2.6875v-5.375c0,-1.48022 -1.20728,-2.6875 -2.6875,-2.6875zM75.25,118.25c-1.48022,0 -2.6875,1.20728 -2.6875,2.6875v5.375c0,1.48022 1.20728,2.6875 2.6875,2.6875c1.48022,0 2.6875,-1.20728 2.6875,-2.6875v-5.375c0,-1.48022 -1.20728,-2.6875 -2.6875,-2.6875zM88.6875,118.25c-1.48022,0 -2.6875,1.20728 -2.6875,2.6875v5.375c0,1.48022 1.20728,2.6875 2.6875,2.6875c1.48022,0 2.6875,-1.20728 2.6875,-2.6875v-5.375c0,-1.48022 -1.20728,-2.6875 -2.6875,-2.6875zM102.125,118.25c-1.48022,0 -2.6875,1.20728 -2.6875,2.6875v5.375c0,1.48022 1.20728,2.6875 2.6875,2.6875c1.48022,0 2.6875,-1.20728 2.6875,-2.6875v-5.375c0,-1.48022 -1.20728,-2.6875 -2.6875,-2.6875zM115.5625,118.25c-1.48022,0 -2.6875,1.20728 -2.6875,2.6875v5.375c0,1.48022 1.20728,2.6875 2.6875,2.6875c1.48022,0 2.6875,-1.20728 2.6875,-2.6875v-5.375c0,-1.48022 -1.20728,-2.6875 -2.6875,-2.6875zM129,118.25c-1.48022,0 -2.6875,1.20728 -2.6875,2.6875v5.375c0,1.48022 1.20728,2.6875 2.6875,2.6875c1.48022,0 2.6875,-1.20728 2.6875,-2.6875v-5.375c0,-1.48022 -1.20728,-2.6875 -2.6875,-2.6875z"></path>
                                        </g>
                                        <path d="" fill="none"></path>
                                        <path d="M86,172c-47.49649,0 -86,-38.50351 -86,-86v0c0,-47.49649 38.50351,-86 86,-86v0c47.49649,0 86,38.50351 86,86v0c0,47.49649 -38.50351,86 -86,86z"
                                              fill="none"></path>
                                        <path d="M86,168.56c-45.59663,0 -82.56,-36.96337 -82.56,-82.56v0c0,-45.59663 36.96337,-82.56 82.56,-82.56v0c45.59663,0 82.56,36.96337 82.56,82.56v0c0,45.59663 -36.96337,82.56 -82.56,82.56z"
                                              fill="none"></path>
                                        <path d="" fill="none"></path>
                                        <path d="" fill="none"></path>
                                    </g>
                                </g>
                            </svg>
                        </div>
                    </div>
                    <div class="row justify-content-center" v-else>
                        <div class="col">
                            <h2 class="text-danger">Failed</h2>
                        </div>
                        <div class="col">
                            <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px"
                                 width="100" height="100"
                                 viewBox="0 0 172 172"
                                 style=" fill:#000000;">
                                <g fill="none" fill-rule="nonzero" stroke="none" stroke-width="1" stroke-linecap="butt"
                                   stroke-linejoin="miter" stroke-miterlimit="10" stroke-dasharray=""
                                   stroke-dashoffset="0"
                                   font-family="none" font-size="none"
                                   style="mix-blend-mode: normal">
                                    <path d="M0,172v-172h172v172z" fill="none"></path>
                                    <g>
                                        <path d="M132.44,20.64c-0.94993,0 -1.72,0.77007 -1.72,1.72c0,0.94993 0.77007,1.72 1.72,1.72c0.94993,0 1.72,-0.77007 1.72,-1.72c0,-0.94993 -0.77007,-1.72 -1.72,-1.72z"
                                              fill="#3498db"></path>
                                        <path d="M86,22.36c-35.1474,0 -63.64,28.4926 -63.64,63.64c0,35.1474 28.4926,63.64 63.64,63.64c35.1474,0 63.64,-28.4926 63.64,-63.64c0,-35.1474 -28.4926,-63.64 -63.64,-63.64z"
                                              fill="#ecf0f1"></path>
                                        <path d="M142.76,18.92c-3.79972,0 -6.88,3.08028 -6.88,6.88c0,3.79972 3.08028,6.88 6.88,6.88c3.79972,0 6.88,-3.08028 6.88,-6.88c0,-3.79972 -3.08028,-6.88 -6.88,-6.88z"
                                              fill="#3498db"></path>
                                        <path d="M149.64,37.84c-1.89986,0 -3.44,1.54014 -3.44,3.44c0,1.89986 1.54014,3.44 3.44,3.44c1.89986,0 3.44,-1.54014 3.44,-3.44c0,-1.89986 -1.54014,-3.44 -3.44,-3.44z"
                                              fill="#e74c3c"></path>
                                        <path d="M139.32,127.28c-1.89986,0 -3.44,1.54014 -3.44,3.44c0,1.89986 1.54014,3.44 3.44,3.44c1.89986,0 3.44,-1.54014 3.44,-3.44c0,-1.89986 -1.54014,-3.44 -3.44,-3.44zM25.8,101.48c-3.79972,0 -6.88,3.08028 -6.88,6.88c0,3.79972 3.08028,6.88 6.88,6.88c3.79972,0 6.88,-3.08028 6.88,-6.88c0,-3.79972 -3.08028,-6.88 -6.88,-6.88z"
                                              fill="#9b59b6"></path>
                                        <path d="M43,146.2c-1.89986,0 -3.44,1.54014 -3.44,3.44c0,1.89986 1.54014,3.44 3.44,3.44c1.89986,0 3.44,-1.54014 3.44,-3.44c0,-1.89986 -1.54014,-3.44 -3.44,-3.44z"
                                              fill="#e74c3c"></path>
                                        <path d="M31.82,84.28c-2.37482,0 -4.3,1.92518 -4.3,4.3c0,2.37482 1.92518,4.3 4.3,4.3c2.37482,0 4.3,-1.92518 4.3,-4.3c0,-2.37482 -1.92518,-4.3 -4.3,-4.3zM136.74,55.04c-1.42489,0 -2.58,1.15511 -2.58,2.58c0,1.42489 1.15511,2.58 2.58,2.58c1.42489,0 2.58,-1.15511 2.58,-2.58c0,-1.42489 -1.15511,-2.58 -2.58,-2.58z"
                                              fill="#ffffff"></path>
                                        <g fill="#ffffff">
                                            <path d="M86,44.032c-23.08329,0 -41.796,18.71271 -41.796,41.796c0,23.08329 18.71271,41.796 41.796,41.796c23.08329,0 41.796,-18.71271 41.796,-41.796c0,-23.08329 -18.71271,-41.796 -41.796,-41.796z"></path>
                                            <path d="M86,128.656c-23.736,0 -43,-19.264 -43,-43c0,-23.736 19.264,-43 43,-43c23.736,0 43,19.264 43,43c0,23.736 -19.264,43 -43,43zM86,45.236c-22.36,0 -40.42,18.232 -40.42,40.42c0,22.188 18.06,40.592 40.42,40.592c22.36,0 40.42,-18.232 40.42,-40.42c0,-22.188 -18.06,-40.592 -40.42,-40.592z"></path>
                                        </g>
                                        <g fill="#e74c3c">
                                            <path d="M85.828,50.912c-19.37857,0 -35.088,15.70943 -35.088,35.088c0,19.37857 15.70943,35.088 35.088,35.088c19.37857,0 35.088,-15.70943 35.088,-35.088c0,-19.37857 -15.70943,-35.088 -35.088,-35.088z"></path>
                                        </g>
                                        <g fill="#e74c3c">
                                            <path d="M86.344,56.588c18.232,0 33.196,14.104 34.572,31.82c0,-0.86 0.172,-1.72 0.172,-2.58c0,-18.92 -15.48,-34.4 -34.744,-34.4c-19.092,0 -34.744,15.48 -34.744,34.4c0,0.86 0,1.72 0.172,2.58c1.376,-17.888 16.168,-31.82 34.572,-31.82z"></path>
                                        </g>
                                        <g fill="#ffffff">
                                            <path d="M119.368,76.712c-0.344,0 -0.688,-0.172 -0.86,-0.688c-0.172,-0.516 -0.344,-1.032 -0.516,-1.548c-0.688,-1.892 -1.548,-3.784 -2.58,-5.504c-0.172,-0.344 -0.172,-0.86 0.344,-1.204c0.344,-0.172 0.86,-0.172 1.204,0.344c1.032,1.892 1.892,3.784 2.58,5.676c0.172,0.516 0.344,1.032 0.516,1.548c0.172,0.516 -0.172,0.86 -0.516,1.032c0,0.344 0,0.344 -0.172,0.344z"></path>
                                        </g>
                                        <g fill="#ffffff">
                                            <path d="M86,121.776c-19.78,0 -35.948,-15.996 -35.948,-35.776c0,-19.78 16.168,-35.776 35.948,-35.776c10.32,0 20.124,4.472 26.832,12.04c0.516,0.516 1.032,1.204 1.548,1.72c0.344,0.344 0.172,0.86 -0.172,1.204c-0.344,0.344 -0.86,0.172 -1.204,-0.172c-0.516,-0.516 -0.86,-1.204 -1.376,-1.72c-6.536,-7.224 -15.824,-11.524 -25.628,-11.524c-18.92,0 -34.228,15.308 -34.228,34.056c0,18.748 15.308,34.056 34.228,34.056c18.92,0 34.228,-15.308 34.228,-34.056c0,-1.72 -0.172,-3.44 -0.344,-5.16c0,-0.516 0.172,-0.86 0.688,-1.032c0.516,0 0.86,0.172 1.032,0.688c0.344,1.72 0.344,3.612 0.344,5.332c0,19.952 -16.168,36.12 -35.948,36.12z"></path>
                                        </g>
                                        <g fill="#ffffff">
                                            <path d="M96.32,98.212c-0.516,0 -1.032,-0.172 -1.548,-0.688l-8.944,-8.944l-8.944,8.944c-0.344,0.344 -0.86,0.688 -1.548,0.688c-0.688,0 -1.032,-0.172 -1.548,-0.688c-0.86,-0.86 -0.86,-2.064 0,-2.924l8.944,-8.944l-8.772,-8.944c-0.86,-0.86 -0.86,-2.064 0,-2.924c0.344,-0.344 0.86,-0.688 1.548,-0.688c0.688,0 1.032,0.172 1.548,0.688l8.944,8.944l8.944,-8.944c0.344,-0.344 0.86,-0.688 1.548,-0.688c0.516,0 1.032,0.172 1.548,0.688c0.516,0.516 0.688,0.86 0.688,1.548c0,0.688 -0.172,1.032 -0.688,1.548l-8.944,8.944l8.944,8.944c0.344,0.344 0.688,0.86 0.688,1.548c0,0.516 -0.172,1.032 -0.688,1.548c-0.516,0.516 -1.204,0.344 -1.72,0.344z"></path>
                                            <path d="M96.32,74.132c0.344,0 0.688,0.172 0.86,0.344c0.516,0.516 0.516,1.204 0,1.72l-9.46,9.46l9.46,9.46c0.516,0.516 0.516,1.204 0,1.72c-0.172,0.172 -0.516,0.344 -0.86,0.344c-0.344,0 -0.688,-0.172 -0.86,-0.344l-9.46,-9.46l-9.46,9.46c-0.172,0.172 -0.516,0.344 -0.86,0.344c-0.344,0 -0.688,-0.172 -0.86,-0.344c-0.516,-0.516 -0.516,-1.204 0,-1.72l9.46,-9.46l-9.46,-9.46c-0.516,-0.516 -0.516,-1.204 0,-1.72c0.172,-0.172 0.516,-0.344 0.86,-0.344c0.344,0 0.688,0.172 0.86,0.344l9.46,9.46l9.46,-9.46c0.172,-0.344 0.516,-0.344 0.86,-0.344M96.32,72.412c-0.86,0 -1.548,0.344 -2.064,0.86l-8.256,8.256l-8.256,-8.256c-0.516,-0.516 -1.376,-0.86 -2.064,-0.86c-0.688,0 -1.548,0.344 -2.064,0.86c-0.516,0.516 -0.86,1.376 -0.86,2.064c0,0.688 0.344,1.548 0.86,2.064l8.256,8.256l-8.256,8.256c-0.516,0.516 -0.86,1.376 -0.86,2.064c0,0.688 0.344,1.548 0.86,2.064c0.516,0.516 1.376,0.86 2.064,0.86c0.688,0 1.548,-0.344 2.064,-0.86l8.256,-8.256l8.256,8.256c0.516,0.516 1.376,0.86 2.064,0.86c0.688,0 1.548,-0.344 2.064,-0.86c0.516,-0.516 0.86,-1.376 0.86,-2.064c0,-0.688 -0.344,-1.548 -0.86,-2.064l-8.256,-8.256l8.256,-8.256c0.516,-0.516 0.86,-1.376 0.86,-2.064c0,-0.688 -0.344,-1.548 -0.86,-2.064c-0.516,-0.688 -1.376,-0.86 -2.064,-0.86z"></path>
                                        </g>
                                    </g>
                                </g>
                            </svg>
                        </div>
                    </div>
                </div>
            </b-modal>
        </div>

    </div>
</template>

<script>
    import {userbookinglist} from "../../urls"
    import axios from "axios";
    import Errormessage from "@/components/Utilities/Errormessage";
    import {receivepayment} from "@/../src/urls";

    export default {
        data() {
            return {
                items: [],
                errors: false,
                errorobj: undefined,

                // for modal content
                user_booking_obj: undefined,
                amount_received: undefined,

                // for table customization
                fields: [
                    "booking_number",
                    "person_name",
                    "pet",
                    "check_in_date",
                    "check_out_date",
                    "booked_on_date",
                    "amount",
                    "payment_done",
                    "receive_payment"
                ],
                //busyFlag used for disabling "paid" and "receive payment" btns on table.
                busyFlag: false,
                //flag is managed after the actual request to backend to update the payment request.
                confirmPaymentPostRequest: false,
                bookingid: undefined,
            }
        },
        created() {
            this.errors = false;
            this.errorobj = undefined;
            axios.get(userbookinglist)
                .then(resp => {
                    this.items = resp.data
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
                        this.errors = true;
                        this.errorobj = {"message": "Oops! No Response was received from the Server, Sorry."};
                        // console.log("The request was made but no response was received, `err.request` is an instance of XMLHttpRequest in the browser and an instance of http.ClientRequest in Node.js");
                        // console.log(err.request);
                    }
                })
        },
        components: {
            Errormessage: Errormessage
        },
        methods: {
            confirmPaymentReceipt(dataobj) {
                this.busyFlag = false;
                this.user_booking_obj = dataobj;
                this.$bvModal.show("confirm-receive-payment");
                this.bookingid = this.user_booking_obj.booking_number
            },
            ok() {
                this.busyFlag = true;
                axios.post(receivepayment, {booking: this.bookingid})
                    .then(() => {
                        this.busyFlag = false;
                        this.confirmPaymentPostRequest = true;
                        this.$bvModal.show("amount-received-success-modal");
                        // this.items = resp.data;
                        this.user_booking_obj.payment_done = true
                        this.user_booking_obj = undefined
                        this.bookingid = undefined
                    })
                    .catch(err => {
                        if (err.response) {
                            /*
                             * The request was made and the server responded with a
                             * status code that falls out of the range of 2xx
                             */
                            this.busyFlag = false;
                            this.confirmPaymentPostRequest = false;
                            this.$bvModal.show("amount-received-success-modal")
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
                            // this.errors = true;
                            // this.errorobj = {"message": "Oops! No Response was received from the Server, Sorry."};
                            this.busyFlag = false;
                            this.confirmPaymentPostRequest = false;
                            this.$bvToast.toast("Please check your Internet Connection.", {
                                title: 'Network Error!',
                                autoHideDelay: 5000,
                            })
                            // console.log("The request was made but no response was received, `err.request` is an instance of XMLHttpRequest in the browser and an instance of http.ClientRequest in Node.js");
                            // console.log(err.request);
                        }
                    })
            },
            cancelops() {
                this.user_booking_obj = undefined;
                this.bookingid = undefined
            }
        }
    }
</script>