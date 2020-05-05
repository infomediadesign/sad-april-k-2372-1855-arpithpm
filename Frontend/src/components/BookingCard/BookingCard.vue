<template>
    <b-card bg-variant="light" class=""
    >
        <b-card-body>
            <b-card-sub-title class="mb-2">Booking #</b-card-sub-title>
            <b-card-title>{{booking.id}}</b-card-title>
            <b-card-text>

            </b-card-text>
        </b-card-body>

        <b-list-group flush>
            <b-list-group-item>Check-in: {{booking.check_in_date}}</b-list-group-item>
            <b-list-group-item>Check-out: {{booking.check_out_date}}</b-list-group-item>
            <b-list-group-item>Booked On: {{booking.booked_on_date}}</b-list-group-item>
            <b-list-group-item>Pet: {{booking.petobj.name}} ({{booking.petobj.breedobj.plan.name}})</b-list-group-item>
            <b-list-group-item>Total Cost: {{booking.total_price}}</b-list-group-item>
            <b-list-group-item>Payment Method: {{booking.paymentobj.name}}</b-list-group-item>
            <b-list-group-item>Payment Satus: {{booking.paymentdone ? "Complete" : "Pending"}}</b-list-group-item>
        </b-list-group>

        <b-card-body>
            <a href="#" class="card-link">Card link</a>
            <a href="#" class="card-link">Another link</a>
        </b-card-body>

        <!--            <b-card-footer>This is a footer</b-card-footer>-->

    </b-card>
</template>

<script>
    export default {
        data() {
            return {}
        },
        props: ["booking",],
        computed: {}
    }
</script>

<style scoped>
    .reducedfont {
        font-size: 20px;
    }
</style>