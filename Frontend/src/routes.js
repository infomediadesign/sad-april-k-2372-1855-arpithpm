import Vue from "vue";
import Home from "./components/Home/Home"
import Signin from "./components/Signin/Signin"
import Signout from "./components/Signout/Signout"
import Signup from "./components/Signup/Signup"
import RequestPasswordReset from "./components/RequestPasswordReset/RequestPasswordReset";
import ResetPassword from "./components/PasswordReset/PasswordReset";
import EmailVerification from "./components/EmailVerification/EmailVerification";
import BookNow from "@/components/BookNow/BookNow";
import store from "@/store/store";
import BookingConfirmed from "./components/BookingConfirmed/BookingConfirmed"
import ReceivePayments from "@/components/ReceivePayments/ReceivePayments";
import UserPets from "@/components/UserPets/UserPets";
import AddNewPet from "@/components/AddNewPet/AddNewPet";
import UserProfile from "@/components/UserProfile/UserProfile";


function proceedIfLoggedIn(to, from, next) {
    // if (Vue.$cookies.isKey("datatoken")) {
    //     store.commit("setUserOnLogin", Vue.$cookies.get("datatoken"));
    //     next()
    // } else {
    //     next({name: "signin"})
    // }
    if (store.state.loggedIn) {
        next()
    } else if (Vue.$cookies.isKey("datatoken")) {
        store.commit("setUserOnLogin", Vue.$cookies.get("datatoken"));
        next()
    } else {
        next({name: "signin"})
    }
}

export const routes = [
    {

        path: "/", component: Home, name: "home", beforeEnter: (to, from, next) => {
            proceedIfLoggedIn(to, from, next)
        }
    },
    {
        path: "/signin", component: Signin, name: "signin",
        // beforeEnter: (to, from, next) => {
        //     if (Vue.$cookies.isKey("datatoken")) {
        //         store.commit("setUserOnLogin", Vue.$cookies.get("datatoken"));
        //         next({name: "home"})
        //     } else {
        //         next({name: "signin"})
        //     }
        // }
    },
    {
        path: "/signup", component: Signup, name: "signup", beforeEnter: (to, from, next) => {
            if (store.state.loggedIn) {
                next({name: "home"})
            }else {
                next()
            }
        }
    },

    {path: "/signout", component: Signout, name: "signout"},
    {path: "/request-password-reset", component: RequestPasswordReset, name: "requestpasswordreset"},
    {path: "/reset/:key", component: ResetPassword, name: "passwordreset"},
    {path: "/verify/:key", component: EmailVerification, name: "emailverify"},
    {
        path: "/booknow", component: BookNow, name: "booknow", beforeEnter: (to, from, next) => {
            proceedIfLoggedIn(to, from, next)
        }
    },
    {
        path: "/booking-confirmed",
        component: BookingConfirmed,
        name: "bookingconfirmed",
        beforeEnter: (to, from, next) => {
            proceedIfLoggedIn(to, from, next)
        }
    },

    {
        path: "/receive-payments",
        component: ReceivePayments,
        name: "receivepayments",
        beforeEnter: (to, from, next) => {
            proceedIfLoggedIn(to, from, next)
        }
    },
    {
        path: "/user-pets",
        component: UserPets,
        name: "userpets",
        beforeEnter: (to, from, next) => {
            proceedIfLoggedIn(to, from, next)
        }
    },
    {
        path: "/add-new-pet",
        component: AddNewPet,
        name: "addnewpet",
        beforeEnter: (to, from, next) => {
            proceedIfLoggedIn(to, from, next)
        }
    },
    {
        path: "/user-profile",
        component: UserProfile,
        name: "userprofile",
        beforeEnter: (to, from, next) => {
            proceedIfLoggedIn(to, from, next)
        }
    },


];



