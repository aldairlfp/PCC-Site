<template>
  <MyQTable 
  title="Militantes" 
  request-direction="http://localhost:8000/api/militant/" 
  v-bind:tableHeaders="columns" 
  />
</template>

<script>
import MyQTable from 'components/MyQTable.vue'

const columns = [
  {
    name: "ci",
    label: "No. Identidad",
    align: "left",
    field: "ci",
    sortable: true,
  },
  {
    name: "militant_name",
    align: "center",
    label: "Nombre",
    field: "name",
    sortable: true,
  },
  {
    name: "first_lastname",
    align: "center",
    label: "Primer Apellido",
    field: "first_lastname",
    sortable: true,
  },
  {
    name: "second_lastname",
    align: "center",
    label: "Segundo Apellido",
    field: "second_lastname",
    sortable: true,
  },
];
const visibilityVar = "hidden"

export default {
  components: {
    MyQTable,
  },
  data() {
    return {
      columns,
      visibilityVar,
      methods: {
        changeVisibility() {
          if (this.visibilityVar == "hidden") {
            this.visibilityVar = "visible"
          }
          else {
            this.visibilityVar = "hidden"
          }
        }
      }
    };

  },
}
</script>

<style lang="sass">
.cardContainer
  visibility: visibilityVar
</style>