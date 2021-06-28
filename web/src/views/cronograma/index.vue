<template>
  <div class="app-container">
    <el-row>
      <el-col class="text-center" :span="24">
        <h1 styles="text-align: center;">Cronograma</h1>
      </el-col>
    </el-row>

    <el-row class="filter-container">
      <el-col :span="12" :xs="24">
        <el-input v-model="listQuery.pesquisa" placeholder="Ação" style="width: 200px;" class="filter-item" />
        <el-button v-waves class="filter-item" type="primary" icon="el-icon-search">
          Pesquisar
        </el-button>
      </el-col>

      <el-col style="display:flex; justify-content:flex-end" :span="12" :xs="24">
        <el-button
          v-waves
          class="filter-item"
          type="primary"
          icon="el-icon-plus"
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
            <el-button type="primary" size="mini" icon="el-icon-edit" @click="handleUpdate(row)">
              Editar
            </el-button>
            <el-button type="danger" size="mini" icon="el-icon-delete" @click="handleDelete(row)">
              Remover
            </el-button>
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
</template>

<script>
// import { mapGetters } from 'vuex'
import waves from '@/directive/waves' // waves directive
import Pagination from '@/components/Pagination' // secondary package based on el-pagination
import * as Schedule from '@/api/schedule'
import { validDateIsInPast } from '@/utils/validate'

export default {
  name: 'DashboardEditor',
  directives: { waves },
  components: { Pagination },
  data() {
    const validateDateIsNotInPast = (rule, value, callback) => {
      if (!value || !validDateIsInPast(value)) {
        callback(new Error('Por favor insira uma data válida'))
      } else {
        callback()
      }
    }
    return {
      form: {
        meet: {
          id: undefined,
          scheduled_to: undefined
        },
        options: {
          datas: [{
            text: 'Hoje',
            onClick(picker) {
              picker.$emit('pick', new Date())
            }
          }, {
            text: 'Amanhã',
            onClick(picker) {
              const date = new Date()
              date.setTime(date.getTime() + 3600 * 1000 * 24)
              picker.$emit('pick', date)
            }
          }, {
            text: 'Próxima semana',
            onClick(picker) {
              const date = new Date()
              date.setTime(date.getTime() + 3600 * 1000 * 24 * 7)
              picker.$emit('pick', date)
            }
          }]
        },
        rules: {
          scheduled_to: [{
            required: true, validator: validateDateIsNotInPast, trigger: 'blur' }]
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
    saveData() {
      // this.$refs['dataForm'].validate((valid) => {
      //   if (valid) {
      //     this.loadings.saveMeet = true

      //     const saveOrAccept = this.form.meet?.id ? Meets.save : Meets.accept

      //     saveOrAccept(this.form.meet).then(() => {
      //     }).finally(() => {
      //       this.loadings.saveMeet = false
      //       this.$message({
      //         message: this.form.meet?.id !== undefined ? 'Agendamento atualizado com sucesso!' : 'Novo paciente agendado com sucesso!',
      //         type: 'success'
      //       })
      //       this.getList()
      //       this.form.meet = {
      //         id: undefined,
      //         scheduled_to: undefined
      //       }
      //       this.$refs['dataForm'].resetFields()
      //     })
      //   }
      // })
    },
    handleUpdate(row) {
      // const { id, scheduled_to } = row
      // this.form.meet = { id, scheduled_to }
      // this.$refs['date-picker'].handleFocus()
    }
  }
}
</script>
