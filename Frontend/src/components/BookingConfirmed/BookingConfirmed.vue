<template>
    <div class="row my-3 w-100 justify-content-center">
        <b-alert :show="dismissCountDown" variant="success" @dismiss-count-down="(val) => dismissCountDown = val">
            <h4 class="alert-heading">Booking Confirmed!</h4>
            <p>
                We will ensure you, your pet will be taken care off with utmost love and care while you are away.
                <br><strong>Thank you.</strong>
            </p>
            <hr>
            <p class="mb-0">
                Redirecting to home page in {{ dismissCountDown }} seconds...
            </p>
        </b-alert>
    </div>
</template>


<script>
    export default {
        data() {
            return {
                dismissCountDown: 5
            }
        },
        watch: {
            dismissCountDown(to) {
                if (to === 0) {
                    this.$router.push({name: "home"})
                }
            }
        }

    }
</script>