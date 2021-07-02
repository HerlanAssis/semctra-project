<template>
  <div class="app-container">
    <div class="dashboard-container">
      <component :is="currentRole" />
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import HealthProfessional from './health_professional'
import Patient from './patient'

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

<style scoped>
  .dashboard-container {
    margin-bottom: 32px;
    flex: 1;
  }
</style>
