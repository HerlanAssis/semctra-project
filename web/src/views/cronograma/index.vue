<template>
  <div class="app-container">
    <div class="page-container">
      <el-row>
        <el-col class="text-center" :span="24">
          <h1 styles="text-align: center;">Cronograma</h1>
        </el-col>
      </el-row>

      <el-row class="filter-container">
        <el-col :span="12" :xs="24">
          <el-input
            v-model="listQuery.pesquisa"
            style="width: 400px;"
            placeholder="Ação"
            class="filter-item"
          >
            <el-button slot="append" v-waves type="primary" icon="el-icon-search">
              Pesquisar
            </el-button>
          </el-input>

        </el-col>

        <el-col style="display:flex; justify-content:flex-end" :span="12" :xs="24">
          <el-button
            v-waves
            type="primary"
            icon="el-icon-plus"
            @click="handleCreate"
          >
            Adicionar novo cronograma
          </el-button>
        </el-col>
      </el-row>

      <el-row>
        <el-table
          v-loading="loadings.schedule"
          :data="lists.schedule"
          border
          fit
          highlight-current-row
          style="width: 100%;"
        >
          <el-table-column min-width="120px" align="center" label="Dia">
            <template slot-scope="{row}">
              <span>
                {{ lists.days[row.week_day] }}
              </span>
            </template>
          </el-table-column>

          <el-table-column min-width="220px" align="center" label="Início - Fim">
            <template slot-scope="{row}">
              <span>
                {{ row.start_time }} - {{ row.end_time }}
              </span>
            </template>
          </el-table-column>

          <el-table-column fixed="right" min-width="120px" align="center" label="Ações">
            <template slot-scope="{row}">
              <el-button type="primary" size="mini" icon="el-icon-edit" @click="handleUpdate(row)" />

              <!-- <el-popconfirm
                title="Tem certeza disso?"
                confirm-button-text="Confirmar"
                cancel-button-text="Cancelar"
                icon="el-icon-info"
                icon-color="red"
              >
              </el-popconfirm> -->
              <el-button type="danger" size="mini" icon="el-icon-delete" @click="handleDelete(row)" />
            </template>
          </el-table-column>
        </el-table>
      </el-row>

      <pagination
        v-show="totalAccepted>0"
        :total="totalAccepted"
        :page.sync="listQuery.page"
        :limit.sync="listQuery.limit"
        @pagination="getList"
      />
    </div>
  </div>
</template>

<script>
// import { mapGetters } from 'vuex'
import waves from '@/directive/waves' // waves directive
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import * as Schedule from '@/api/schedule'

export default {
  name: 'DashboardEditor',
  directives: { waves },
  components: { Pagination },
  data() {
    return {
      popoverDelete: false,
      form: {
        meet: {
          id: undefined,
          scheduled_to: undefined
        }
      },
      lists: {
        schedule: [],
        days: {}
      },
      loadings: {
        schedule: false,
        days: false
      },
      listQuery: {
        pesquisa: '',
        page: 1,
        limit: 10,
        importance: undefined,
        title: undefined,
        type: undefined,
        sort: '+id'
      }
    }
  },
  computed: {
    totalAccepted() {
      return this.lists.schedule.length
    },
    totalPending() {
      return this.lists.schedule.length
    }
  },
  created() {
    this.getList()
    this.getDaysList()
  },
  methods: {
    getList() {
      this.loadings.schedule = true
      Schedule.getList().then(response => {
        this.lists.schedule = response.data
      }).finally(() => {
        this.loadings.schedule = false
      })
    },
    getDaysList() {
      this.loadings.days = true
      Schedule.getDays().then(response => {
        this.lists.days = response.data
      }).finally(() => {
        this.loadings.days = false
      })
    },
    handleCreate() {
      this.$router.push({ name: 'CadastrarCronograma' })
    },
    handleUpdate(row) {
      const { id } = row
      this.$router.push({ name: 'EditarCronograma', params: { id }})
    },
    handleDelete(row) {
      const loading = this.$loading({
        lock: true,
        text: 'Loading',
        spinner: 'el-icon-loading'
      })

      Schedule.remove({ id: row.id }).then(() => {
        this.$notify({
          title: 'Sucesso',
          message: 'Dados removidos com sucesso',
          type: 'success'
        })

        this.getList()
      }).finally(() => loading.close())
    }
  }
}
</script>
