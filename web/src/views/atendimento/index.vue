<template>
  <div class="dashboard-container">
    <component :is="currentRole" />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import HealthProfessional from './health_professional'
import Patient from './patient'

// TODO criar um mixin para melhorar a leitura dos arquivos de pacient e health_professional
export default {
  name: 'Dashboard',
  components: { HealthProfessional, Patient },
  data() {
    return {
      currentRole: 'HealthProfessional'
    }
  },
  computed: {
    ...mapGetters([
      'roles'
    ])
  },
  created() {
    if (!this.roles.includes('HEALTH_PROFESSIONAL')) {
      this.currentRole = 'Patient'
    }
  }
}
</script>
