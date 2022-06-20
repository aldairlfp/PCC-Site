<template>
<q-page class="flex flex-center">

</q-page>
</template>

<script>
import { ref } from "vue";
import axios from "axios";
import { useQuasar } from "quasar";
import { Notify } from "quasar";
import { useMeta } from "quasar";

export default{
  methods: {
    get_cores() {
      this.$axios
        .get("http://localhost:8000/api/core/")
        .then((res) => {
          this.rows = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    reloadPage() {
      window.location.reload();
    },
    addRow() {
      this.$router.push("./addcore");
    },
    modifyRow() {},
  },
}
</script>
