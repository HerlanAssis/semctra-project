<template>
  <div class="components-container">
    <el-row>
      <el-col class="text-center" :span="24">
        <h1 styles="text-align: center;">Atendimentos</h1>
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
        <el-form
          ref="dataForm"
          :rules="form.rules"
          :model="form.meet"
          label-position="left"
          :inline="true"
        >
          <el-form-item label="Agendar novo atendimento para" prop="scheduled_to">
            <el-date-picker
              ref="date-picker"
              v-model="form.meet.scheduled_to"
              format="dd/MM/yyyy HH:mm"
              type="datetime"
              placeholder="Selecione o dia e a hora"
              :picker-options="form.options.datas"
            />
          </el-form-item>
          <el-form-item>
            <el-tooltip class="item" effect="dark" content="Salvar" placement="bottom">

              <el-button
                class="filter-item"
                style="margin-left: 10px;"
                type="primary"
                plain
                icon="el-icon-check"
                :loading="loadings.saveMeet"
                @click="saveData"
              />
            </el-tooltip>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>

    <el-table
      v-loading="loadings.meetsAccepted"
      :data="meetsAccepted"
      border
      fit
      highlight-current-row
      style="width: 100%;"
    >
      <el-table-column min-width="120px" align="center" label="Paciente">
        <template slot-scope="{row}">
          <span>
            {{ row.requester.username }}
          </span>
        </template>
      </el-table-column>

      <el-table-column min-width="200px" align="center" label="Horário de atendimento">
        <template slot-scope="{row}">
          <span>
            {{ row.scheduled_to }}
          </span>
        </template>
      </el-table-column>

      <el-table-column fixed="right" min-width="120px" align="center" label="Ações">
        <template slot-scope="{row}">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">
            Editar
          </el-button>
          <el-button @click="$router.push({name:'Meet', params:{id:row.id}})" :disabled="!row.token" type="success" size="mini" icon="el-icon-video-camera">
            Chamada de Vídeo
          </el-button>
        </template>
      </el-table-column>
    </el-table>

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
import * as Meets from '@/api/meet'
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
      openMeetFormDialog: false,
      meetsAccepted: [],
      loadings: {
        meetsAccepted: false,
        saveMeet: false
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
      return this.meetsAccepted.length
    },
    totalPending() {
      return this.meetsAccepted.length
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.loadings.meetsAccepted = true
      Meets.getList().then(response => {
        this.meetsAccepted = response.data
      }).finally(() => {
        this.loadings.meetsAccepted = false
      })
    },
    saveData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          this.loadings.saveMeet = true

          const saveOrAccept = this.form.meet?.id ? Meets.save : Meets.accept

          saveOrAccept(this.form.meet).then(() => {
          }).finally(() => {
            this.loadings.saveMeet = false
            this.$message({
              message: this.form.meet?.id !== undefined ? 'Agendamento atualizado com sucesso!' : 'Novo paciente agendado com sucesso!',
              type: 'success'
            })
            this.getList()
            this.form.meet = {
              id: undefined,
              scheduled_to: undefined
            }
            this.$refs['dataForm'].resetFields()
          })
        }
      })
    },
    handleUpdate(row) {
      const { id, scheduled_to } = row
      this.form.meet = { id, scheduled_to }
      this.$refs['date-picker'].handleFocus()
    }
  }
}
</script>

