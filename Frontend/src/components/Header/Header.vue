<template>
    <b-navbar type="dark" variant="primary">
        <b-navbar-brand href="#" to="/">Domigo</b-navbar-brand>
        <b-collapse id="nav-collapse" is-nav>
            <!-- Right aligned nav items -->
            <b-navbar-nav class="ml-auto">
                <b-nav-item exact-active-class="text-white" :to="{name: 'signin'}" exact v-if="!loggedIn">Login
                </b-nav-item>
                <b-nav-item exact-active-class="text-white" :to="{name: 'signup'}" exact v-if="!loggedIn">Signup
                </b-nav-item>
                <b-nav-item exact-active-class="text-white" :to="{name: 'home'}" exact v-if="loggedIn">Home</b-nav-item>
                <b-nav-item exact-active-class="text-white" :to="{name: 'booknow'}" exact v-if="loggedIn">Book Now
                </b-nav-item>
                <b-nav-item exact-active-class="text-white" :to="{name: 'receivepayments'}" exact v-if="loggedIn">
                    Payments
                </b-nav-item>
                <b-nav-item-dropdown right v-if="loggedIn">
                    <template v-slot:button-content>
                        <span>{{$store.state.userdata.first_name}}</span>
                    </template>
                    <b-dropdown-item href="#" :to="{name: 'userprofile'}">Account</b-dropdown-item>
                    <b-dropdown-item href="#" :to="{name: 'userpets'}">My Pets</b-dropdown-item>
                    <hr class="my-0 border-danger">
                    <b-dropdown-item :to="{name: 'signout'}" exact variant="danger">Logout</b-dropdown-item>
                </b-nav-item-dropdown>
            </b-navbar-nav>
        </b-collapse>
    </b-navbar>
</template>


<script>
    import {mapState} from "vuex";

    export default {
        data() {
            return {}
        },


        computed: mapState({
            loggedIn: state => state.loggedIn
        }),
    }
</script>

