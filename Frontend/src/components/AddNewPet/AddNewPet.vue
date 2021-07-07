<template>
    <div class="col-md-12">
        <h4>Add New Pet</h4>
        <hr>
        <div class="row justify-content-center">
            <div class="col-md-6">
                <Errormessage v-if="errorobj" :errorobj="errorobj"></Errormessage>
                <b-overlay :show="breedlistdata.length < 1 || loading" rounded="sm" spinner-variant="primary">
                    <b-card header="Pet Details">
                        <b-form v-if="show" @submit="onSubmit" @reset="onReset">
                            <div class="row">
                                <div class="col">
                                    <b-form-group
                                            id="input-group-1"
                                            label="Pet Category:"
                                            label-for="input-1">
                                        <b-form-select
                                                id="input-1"
                                                v-model="form.category"
                                                required
                                                :options="petcategoryOptions"
                                                placeholder="Select Category"
                                        ></b-form-select>
                                    </b-form-group>
                                </div>
                                <div class="col">
                                    <b-form-group
                                            label="Breed:"
                                            label-for="breedid">
                                        <b-form-select
                                                id="breedid"
                                                v-model="form.breed"
                                                required
                                                :options="breedOptions"
                                                placeholder="Select Category"
                                        ></b-form-select>
                                    </b-form-group>
                                </div>
                            </div>
                            <div>
                                <b-form-group id="input-group-2" label="Pet Name:" label-for="input-2">
                                    <b-form-input
                                            id="input-2"
                                            v-model="form.name"
                                            required
                                            placeholder="Enter Pet name"
                                    ></b-form-input>
                                </b-form-group>
                                <b-form-group label="Instructions for handling your Pet:" label-for="instructions">
                                    <b-form-input
                                            id="instructions"
                                            v-model="form.instructions"
                                            required
                                            placeholder="Pet Instructions"
                                    ></b-form-input>
                                </b-form-group>

                                <b-form-group label="Date of Birth(Approximate):" label-for="instructions">
                                    <v-date-picker
                                            :max-date='new Date()'
                                            v-model="rawDob"
                                            is-inline/>
                                </b-form-group>
                                <b-button type="submit" variant="primary" class="mx-1">Submit</b-button>
                                <b-button type="reset" variant="danger" class="mx-1">Reset</b-button>
                            </div>
                        </b-form>
                    </b-card>
                </b-overlay>
            </div>
        </div>

    </div>
</template>

<script>
    import {petcategory, breedlist, userpets} from "@/urls";
    import moment from "moment";
    import DatePicker from 'v-calendar/lib/components/date-picker.umd'

    import axios from "axios";
    import Errormessage from "@/components/Utilities/Errormessage";

    export default {
        props: {},
        data() {
            return {
                form: {
                    category: '',
                    breed: "",
                    name: '',
                    instructions: "",
                    date_of_birth: "",
                },
                rawDob: "",
                show: true,
                petcategoryOptions: undefined,
                breedlistdata: undefined,
                // for options of breed select/dropdown in form.
                breedOptions: undefined,
                errorobj: false,
                loading: false
            }
        },
        beforeCreate() {
            axios.get(petcategory)
                .then(res => {
                    this.petcategoryOptions = res.data.map(item => {
                        return {text: item.name, value: item.id}
                    })
                });
            axios.get(breedlist)
                .then(res => {
                    this.breedlistdata = res.data
                })
        },
        methods: {
            onReset(evnt) {
                evnt.preventDefault();
                this.form.category = null;
                this.form.breed = null;
                this.form.name = null;
                this.form.instructions = null;
                this.form.date_of_birth = null;
                this.rawDob = null;
                this.errorobj = false
            },
            onSubmit(event) {
                event.preventDefault();
                this.errorobj = false;
                if (this.rawDob instanceof Date) {
                    this.loading = true
                    // send post request
                    axios.post(userpets, {...this.form})
                        .then(() => {
                            this.$bvModal.msgBoxOk("Pet Details added.").then(() => {
                                this.$router.push({name: "userpets"})
                            })
                        })
                        .catch(err => this.errorobj = err.response.data)
                        .then(() => this.loading = false)
                } else {
                    this.errorobj = {"Date": "Select a valid Date."}
                }
            }
        },
        watch: {
            'rawDob': function (val) {
                console.log(val);
                this.form.date_of_birth = moment(val).format("YYYY-MM-DD")
            },
            'form.category': function (val) {
                this.breedOptions = [];
                this.form.breed = undefined;
                this.breedOptions = this.breedlistdata.map(function (item) {
                    if (item.category.id === val) {
                        return {text: item.name, value: item.id}
                    }
                });
                this.breedOptions = this.breedOptions.filter(function (item) {
                    return item !== undefined
                })
            }
        },
        components: {
            "v-date-picker": DatePicker,
            Errormessage: Errormessage

        }
    };
</script>
