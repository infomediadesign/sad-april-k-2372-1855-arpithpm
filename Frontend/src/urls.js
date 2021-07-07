let base_url = "";

if (process.env.NODE_ENV === "development") {
    base_url = "http://127.0.0.1:8000/";
} else {
    base_url = "https://domigo.herokuapp.com/";
}

export const baseurl = base_url;
export const login = base_url + "accounts/login/";
export const signup = base_url + "accounts/register/";
export const requestpasswordreset = base_url + "accounts/request-password-reset/";
export const resetpassword = base_url + "accounts/reset-password/";
export const emailverification = base_url + "accounts/verify-email/";
export const pastbookings = base_url + "api/pastbookings/";
export const newbooking = base_url + "api/newbooking/";
export const userpets = base_url + "api/userpets/";
export const paymentmethods = base_url + "api/paymentmethods/";
export const petcategory = base_url + "api/petcategory/";
export const breedlist = base_url + "api/breedlist/";
export const userprofile = base_url + "accounts/profile/";

// for the admin users only
export const userbookinglist = baseurl + "api/admin/userbookings/";
export const receivepayment = baseurl + "api/admin/receive-payment/";
