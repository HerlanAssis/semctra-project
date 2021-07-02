<template>
  <div class="app-container">
    <div class="page-container">
      <div class="title-container">
        <typography convention="main-title">
          Cronograma
        </typography>
      </div>

      <div class="form-container">

        <el-form ref="form" label-width="auto" label-position="top" :model="form">
          <el-form-item prop="week" label="Dia da semana">
            <el-select v-model="form.week" filterable placeholder="Dia da Semana">
              <el-option
                v-for="item in weekList"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
          <el-form-item prop="range" label="Intervalo">
            <el-time-picker
              v-model="form.range"
              arrow-control
              is-range
              range-separator="Até"
              start-placeholder="Início"
              end-placeholder="Fim"
            />
          </el-form-item>
          <el-form-item>
            <el-row type="flex" justify="space-between">
              <div>
                <el-button @click="onClean">Limpar</el-button>
              </div>

              <div>
                <el-button type="danger" @click="onCancel">Cancelar</el-button>
                <el-button type="primary" @click="onSave">Salvar</el-button>
              </div>
            </el-row>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
import * as Schedule from '@/api/schedule'
import Typography from '@/components/Typography'

export default {
  name: 'ScheduleForm',
  components: {
    Typography
  },
  data() {
    const dateNow = new Date()
    const dateNowMore1Hour = new Date()
    dateNowMore1Hour.setHours(dateNowMore1Hour.getHours() + 1)

    return {
      form: {
        range: [dateNow, dateNowMore1Hour],
        week: ''
      },
      week: {
        list: [],
        loading: false
      }
    }
  },
  computed: {
    currentID() {
      return this.$route?.params?.id
    },
    crudType() {
      return this.currentID ? 'update' : 'create'
    },
    weekList() {
      return Object.entries(this.week.list).map(([value, label]) => ({ label, value }))
    }
  },
  created() {
    if (this.crudType === 'update') {
      this.getDetail(this.currentID)
    }

    this.getListOptions()
  },
  methods: {
    getListOptions() {
      this.week.loading = true
      Schedule.getDays().then(response => {
        this.week.list = response.data
      }).finally(() => {
        this.week.loading = false
      })
    },
    getDetail(id) {
      this.week.loading = true
      Schedule.get({ id }).then(response => {
        const { week_day, start_time, end_time } = response.data

        const [sHour, sMinutes, sSeconds] = start_time.split(':')
        const [eHour, eMinutes, eSeconds] = end_time.split(':')

        const sTime = new Date()
        sTime.setHours(sHour)
        sTime.setMinutes(sMinutes)
        sTime.setSeconds(sSeconds)

        const eTime = new Date()
        eTime.setHours(eHour)
        eTime.setMinutes(eMinutes)
        eTime.setSeconds(eSeconds)

        this.form = {
          week: week_day,
          range: [sTime, eTime]
        }
      }).finally(() => {
        this.week.loading = false
      })
    },
    onCancel() {
      this.$router.back()
    },
    onClean() {
      this.$refs['form'].resetFields()
    },
    onSave() {
      const loading = this.$loading({
        lock: true,
        text: 'Loading',
        spinner: 'el-icon-loading'
      })

      this.$refs['form'].validate((valid) => {
        if (valid) {
          const [sTime, eTime] = this.form.range

          const data = {
            id: this.currentID,
            week_day: this.form.week,
            start_time: `${sTime.getHours()}:${sTime.getMinutes()}:${sTime.getSeconds()}`,
            end_time: `${eTime.getHours()}:${eTime.getMinutes()}:${eTime.getSeconds()}`
          }

          Schedule.save(data).then(() => {
            this.$notify({
              title: 'Sucesso',
              message: 'Dados salvos com sucesso',
              type: 'success'
            })
          }).finally(() => loading.close())
        }
      })
    }
  }
}
</script>

