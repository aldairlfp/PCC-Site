<template>
    <div class="q-pa-md">

        <center>
            <div class="table-header text-h4">{{ title }}</div>
        </center>

        <q-table class="my-sticky-header-column-table my-table-style" :rows="rows" :columns="tableHeaders" row-key="ci"
            :filter="filter" selection="single" v-model:selected="selected" :separator="separator">
            <template v-slot:top>
                <q-btn color="primary" :disable="loading" label="Agregar" @click="fixed = true" />
                <q-btn class="q-ml-sm" color="primary" :disable="loading" label="Modificar" @click="modifyRow" />
                <q-btn class="q-ml-sm" color="accent" :disable="loading" label="Eliminar" @click="persistent = true" />
                <q-space />
                <q-input borderless dense debounce="300" color="primary" v-model="filter">
                    <template v-slot:append>
                        <q-icon name="search" />
                    </template>
                </q-input>
            </template>
        </q-table>

        <div class="q-pa-md q-gutter-sm">
            <q-dialog v-model="fixed">
                <q-card>
                    <q-card-section>
                        <div class="text-h6">Terms of Agreement</div>
                    </q-card-section>

                    <q-separator />

                    <q-card-section style="max-height: 50vh" class="scroll">
                        <p v-for="n in 15" :key="n">Lorem ipsum dolor sit amet consectetur adipisicing elit. Rerum
                            repellendus sit voluptate voluptas eveniet porro. Rerum blanditiis perferendis totam, ea at
                            omnis vel numquam exercitationem aut, natus minima, porro labore.</p>
                    </q-card-section>

                    <q-separator />

                    <q-card-actions align="right">
                        <q-btn flat label="Decline" color="primary" v-close-popup />
                        <q-btn flat label="Accept" color="primary" v-close-popup />
                    </q-card-actions>
                </q-card>
            </q-dialog>
        </div>

        <div class="q-pa-md q-gutter-sm">
            <q-dialog v-model="persistent" persistent transition-show="scale" transition-hide="scale">
                <q-card class="deleting-card text-black" style="width: 300px">
                    <q-card-section>
                        <div class="text-h5">Alerta !!!</div>
                    </q-card-section>

                    <q-card-section class="q-pt-none">
                        Esta Acción es irreversible. Está seguro que desea continuar ?
                    </q-card-section>

                    <q-card-actions align="right" class="bg-white text-teal">
                        <q-btn class="q-ml-sm" color="accent" label="Continuar" v-close-popup @click="removeRow" />
                        <q-btn class="q-ml-sm" color="primary" label="Cancelar" v-close-popup />
                    </q-card-actions>
                </q-card>
            </q-dialog>
        </div>
    </div>
</template>

<script>
import { Notify } from 'quasar'
import { defineComponent, ref } from "vue";
import axios from "src/boot/axios";
import { Cookies } from "quasar";

export default ({
    props: {
        'title': String,
        'requestDirection': String,
        'tableHeaders': Array,
        'visibilityVar': String,
    },
    data() {
        return {

            persistent: ref(false),
            basic: ref(false),
            fixed: ref(false),

            selected: ref([]),
            rows: [],
            loading: ref(false),
            filter: ref(""),
            rowCount: ref(10),
            separator: ref("cell"),
            lorem: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
        };
    },
    methods: {
        getData() {
            const token = Cookies.get('auth-token')
            this.$axios
                .get(this.requestDirection, {
                    headers: {
                        'Authorization': 'Token ' + token,
                    }
                })
                .then((res) => {
                    this.rows = res.data;
                    console.log(res);
                })
                .catch((err) => {
                    console.log(err);
                });
        },
        verifyAuth() {
            if (!Cookies.has('auth-token')) {
                this.$router.push('/')
                return
            }
        },
        addRow() {

        },
        removeRow() {
            try {
                const token = Cookies.get('auth-token')
                console.log(this.requestDirection + this.selected[0].ci)
                this.$axios.delete(
                    this.requestDirection + this.selected[0].ci, {
                    headers: {
                        'Authorization': 'Token ' + token,
                    }
                })
            }
            catch {
                Notify.create({
                    message: 'Debe seleccionar la fila a borrar',
                    icon: "highlight_off",
                    color: "accent",
                })
            }
            // window.location.reload();
        },
        modifyRow() {

        },
    },
    mounted() {
        this.verifyAuth()
        this.getData();
    },
});
</script>

<style lang="sass">
.deleting-card
.table-header
    color: #FFFFFF
    background-color: $primary
    border-radius: 20px 20px 0px 0px
    max-width: 100%

.q-checkbox__inner
  color: $accent

.text-grey-8
  color: $accent

.my-sticky-header-column-table
  /* height or max-height is important */
  max-height: 500px

  /* specifying max-width so the example can
    highlight the sticky column on any browser window */
  max-width: 100%

  td:first-child
    /* bg color is important for td; just specify one */
    background-color: $secondary !important

  tr th
    position: sticky
    /* higher than z-index for td below */
    z-index: 2
    /* bg color is important; just specify one */
    background: $primary
    color: #fff

  /* this will be the loading indicator */
  thead tr:last-child th
    /* height of all previous header rows */
    top: 48px
    /* highest z-index */
    z-index: 3
  thead tr:first-child th
    top: 0
    z-index: 1
  tr:first-child th:first-child
    /* highest z-index */
    z-index: 3

  td:first-child
    z-index: 1

  td:first-child, th:first-child
    position: sticky
    left: 0
</style>