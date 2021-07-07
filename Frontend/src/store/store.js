import Vue from "vue";
import Vuex from "vuex";

const jwtDecode = require('jwt-decode');


Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        loggedIn: false,
        userdata: undefined
    },
    mutations: {
        setUserOnLogin(state, token) {
            state.loggedIn = true;
            state.userdata = jwtDecode(token.token);
            state.userdata.token = token.token;
            Vue.$cookies.set("datatoken", token, "1d");
        },

        setUsernameOnProfileUpdate(state, name) {
            state.userdata.first_name = name
        },

        logoutuser(state) {
            let cookies = Vue.$cookies.keys();
            for (let i = 0; i < cookies.length; i++) {
                Vue.$cookies.remove(cookies[i])
            }
            state.loggedIn = false;
            state.userdata = undefined

        }
    }

})