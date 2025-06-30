<template>
  <div>
    <h2>Gestion des permissions par sous-rôle</h2>
    <div v-for="subRole in subRoles" :key="subRole.id" class="subrole-block">
      <h3>{{ subRole.name }}</h3>
      <ul>
        <li v-for="perm in allPermissions" :key="perm.id">
          <label>
            <input type="checkbox"
                   :checked="hasPermission(subRole, perm)"
                   @change="togglePermission(subRole, perm, $event.target.checked)">
            {{ perm.name }}
          </label>
        </li>
      </ul>
    </div>
    <button @click="saveChanges">Enregistrer les modifications</button>
    <div v-if="successMessage" class="success">{{ successMessage }}</div>
    <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
  </div>
</template>

<script>
export default {
  name: 'PermissionManagement',
  data() {
    return {
      subRoles: [],
      allPermissions: [],
      subRolePermissions: {}, // {subRoleId: [permId, ...]}
      successMessage: '',
      errorMessage: ''
    }
  },
  async mounted() {
    try {
      // À adapter selon vos endpoints réels
      this.subRoles = await fetch('/api/auth/sub-roles/').then(r => r.json())
      this.allPermissions = await fetch('/api/auth/permissions/').then(r => r.json())
      // Charger les permissions actuelles par sous-rôle
      const perms = await fetch('/api/auth/sub-permissions/').then(r => r.json())
      // Formatage pour accès rapide
      this.subRolePermissions = {}
      perms.forEach(p => {
        if (!this.subRolePermissions[p.sub_role]) this.subRolePermissions[p.sub_role] = [];
        this.subRolePermissions[p.sub_role].push(p.permission)
      })
    } catch (e) {
      this.errorMessage = "Erreur lors du chargement des données."
    }
  },
  methods: {
    hasPermission(subRole, perm) {
      return this.subRolePermissions[subRole.id]?.includes(perm.id)
    },
    togglePermission(subRole, perm, checked) {
      if (!this.subRolePermissions[subRole.id]) this.subRolePermissions[subRole.id] = []
      if (checked) {
        if (!this.subRolePermissions[subRole.id].includes(perm.id))
          this.subRolePermissions[subRole.id].push(perm.id)
      } else {
        this.subRolePermissions[subRole.id] = this.subRolePermissions[subRole.id].filter(id => id !== perm.id)
      }
    },
    async saveChanges() {
      try {
        // À adapter selon vos endpoints et payloads
        await fetch('/api/auth/sub-permissions/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.subRolePermissions)
        })
        this.successMessage = "Permissions mises à jour avec succès."
        this.errorMessage = ''
      } catch (e) {
        this.errorMessage = "Erreur lors de la sauvegarde."
        this.successMessage = ''
      }
    }
  }
}
</script>

<style scoped>
.subrole-block { margin-bottom: 2rem; }
.success { color: green; }
.error { color: red; }
</style>
