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
        <el-button
          v-waves
          class="filter-item"
          type="primary"
          icon="el-icon-plus"
          @click="solicitarDialogVisible = true"
        >
          Solicitar novo atendimento
        </el-button>
      </el-col>
    </el-row>

    <el-table
      v-loading="loadings.meets"
      :data="meets"
      border
      fit
      highlight-current-row
      style="width: 100%;"
    >

      <el-table-column min-width="200px" align="center" label="Horário de atendimento">
        <template slot-scope="{row}">
          <span v-if="row.scheduled_to">
            {{ row.scheduled_to }}
          </span>
          <span v-else>
            ----
          </span>
        </template>
      </el-table-column>

      <el-table-column fixed="right" min-width="120px" align="center" label="Status">
        <template slot-scope="{row}">
          <span>{{row.status}}</span>          
        </template>
      </el-table-column>

      <el-table-column fixed="right" min-width="120px" align="center" label="Ações">
        <template slot-scope="{row}">
          <!-- <el-button type="primary" size="mini" @click="handleUpdate(row)">
            Editar
          </el-button> -->
          <el-button @click="$router.push({name:'Meet', params:{id:row.id}})" :disabled="!row.token" type="success" size="mini" icon="el-icon-video-camera">
            Chamada de Vídeo
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog
      title="Confirmar solicitação"
      :visible.sync="solicitarDialogVisible"
      width="30%"
      center
    >
      <span>Deseja solicitar um atendimento com um profissional de saúde?</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="solicitarDialogVisible = false">Não</el-button>
        <el-button :loading="loadings.saveMeet" type="primary" @click="solicitarAtendimento">Sim, quero solicitar</el-button>
      </span>
    </el-dialog>

    <pagination
      v-show="total>0"
      :total="total"
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

export default {
  name: 'DashboardEditor',
  directives: { waves },
  components: { Pagination },
  data() {
    return {
      solicitarDialogVisible: false,
      meets: [],
      loadings: {
        meets: false,
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
    total() {
      return this.meets.length
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.loadings.meets = true
      Meets.getList().then(response => {
        this.meets = response.data
      }).finally(() => {
        this.loadings.meets = false
      })
    },
    solicitarAtendimento() {
      Meets.save().then(() => {
      }).finally(() => {
        this.loadings.saveMeet = false
        this.$message({
          message: 'Novo agendamento solicitado com sucesso!',
          type: 'success'
        })
        this.getList()
        this.solicitarDialogVisible = false
      })
    }
  }
}
</script>

