<template>
  <div>
    <panel-group @handleSetLineChartData="handleSetLineChartData" />

    <el-row :gutter="0" class="page-container">
      <el-col class="card-info card-avatar" :span="3">
        <el-avatar size="small" :src="circleUrl" />
      </el-col>

      <el-col class="card-info patient-detail" :span="17">
        <el-row>
          <el-col :span="12">
            <typography convention="small-title">
              Nome: <typography convention="title">Maria Antônia da Silva</typography>
            </typography>
          </el-col>
          <el-col :span="12">
            <typography convention="small-title">
              Idade: <typography convention="title">50 anos</typography>
            </typography>
          </el-col>
        </el-row>

        <el-row>
          <el-col :span="24">
            <typography convention="title">
              Motivo do Atendimento:
            </typography>
          </el-col>
          <el-col :span="24">
            <typography>
              Paciente diz sentir fortes dores na cabeça, tontoras e enjoos.
            </typography>
          </el-col>
        </el-row>

      </el-col>

      <el-col class="card-info card-action" :span="4">
        <div class="card-action-icon-wrapper icon-phone-call" @click="getNextMeet">
          <svg-icon icon-class="phone-call" class-name="card-action-icon" />
        </div>

        <!-- TODO: modal com dados clíncos do paciente  -->
        <div class="card-action-icon-wrapper icon-more">
          <svg-icon icon-class="more" class-name="card-action-icon" />
        </div>
      </el-col>
    </el-row>
  </div>

</template>

<script>
import { mapGetters } from 'vuex'
import PanelGroup from '../components/PanelGroup'
import Typography from '@/components/Typography'
import * as Meets from '@/api/meet'

export default {
  name: 'DashboarHealthProfessional',
  components: {
    Typography,
    PanelGroup
  },
  data() {
    return {
      circleUrl: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
      meets: {
        loading: false,
        list: []
      }
    }
  },
  computed: {
    ...mapGetters([
      'name',
      'avatar',
      'roles'
    ]),
    loading() {
      return this.meets.loading
    }
  },
  watch: {
    loading(newVal) {
      if (newVal) {
        this.$loading({
          lock: true,
          text: 'Loading',
          spinner: 'el-icon-loading'
        })
      } else {
        this.$loading().close()
      }
    }
  },
  methods: {
    handleSetLineChartData(type) {
      // this.lineChartData = lineChartData[type]
    },
    async getNextMeet() {
      const { data } = await Meets.accept({ scheduled_to: new Date().toLocaleString() })
      if (data.id) {
        this.$router.push({ name: 'Meet', params: { id: data.id }})
      }
    }
  }
}
</script>

<style lang="scss" scoped>

.card-info {
  height: 100px;
}

.card-avatar {
  display: flex;
  align-items: center;
  justify-content: center;

  .el-avatar {
    height: 90px;
    width: 90px;
  }
}

.card-action {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-left: 10px !important;

  .icon-phone-call {
    color: #40c9c6;

    &:hover {
      cursor: pointer;
      color: white;
      background: #40c9c6;
    }
  }

  .icon-more {
    color: #36a3f7;

    &:hover {
      cursor: pointer;
      color: white;
      background: #36a3f7;
    }

    transform: rotate(90deg);
  }

  .card-action-icon-wrapper {
    float: left;
    margin: 14px 0 0 14px;
    padding: 16px;
    transition: all 0.38s ease-out;
    border-radius: 40px;
  }

  .card-action-icon {
    float: left;
    font-size: 48px;
  }

}

.patient-detail {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  padding: 0 0 10px 10px !important;

  border: 1px solid #DFE6EC;
  border-top: 0;
  border-bottom: 0;
}
</style>
