<template>
    <div class="container">
        <div class="row">
            <div class="col" align="center">
                <b-overlay :show="show" rounded="sm">
                    <div class="col my-5" align="center">
                        <b-spinner variant="primary" label="Spinning"></b-spinner>
                        <h5 class="my-5">Please wait...</h5>
                    </div>
                </b-overlay>

            </div>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                show: false
            }
        },
        mounted() {
            this.$store.commit("logoutuser");
            this.$router.push("signin")
        }
    }
</script>