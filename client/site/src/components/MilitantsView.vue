<template>
    <div class="militant_container">
        <div class="militant_content">
            <h1>Militantes</h1>
            <ul class="militant_list">
                <li v-for="militant in militants" :key="militant.id">
                    <h3>{{ militant }}</h3>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
// import "jquery/dist/jquery.min.js";
// import "bootstrap/dist/css/bootstrap.min.css";
// import "datatables.net-dt/js/dataTables.dataTables";
// import "datatables.net-dt/css/jquery.dataTables.min.css";
import axios from "axios";
// import $ from "jquery";
export default {
        data() {
            return {
                // tasks
                militants: ['']
            }
        },
        methods: {
            async getData() {
                try {
                    // fetch tasks
                    const response = await axios.get('http://localhost:8000/pcc/militant/');
                    // set the data returned as tasks
                    this.militants = response.data; 
                } catch (error) {
                    // log the error
                    console.log(error);
                }
            },
        },
        created() {
            // Fetch tasks on page load
            this.getData();
        }
    }
</script>