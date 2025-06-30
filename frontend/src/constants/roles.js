// Rôles principaux
export const ROLES = {
  SUPER_ADMIN: 'SUPER_ADMIN',
  ADMIN: 'ADMIN',
  DOCTOR: 'DOCTOR',
  SPECIALIST: 'SPECIALIST',
  RADIOLOGIST: 'RADIOLOGIST',
  TECHNICIAN: 'TECHNICIAN',
  BLOOD_BANK_MANAGER: 'BLOOD_BANK_MANAGER',
  NURSE: 'NURSE',
  PATIENT: 'PATIENT'
};

// Groupes de rôles pour les autorisations
export const ROLE_GROUPS = {
  ADMINISTRATORS: ['SUPER_ADMIN', 'ADMIN'],
  MEDICAL_STAFF: ['DOCTOR', 'SPECIALIST', 'RADIOLOGIST', 'NURSE'],
  IMAGING_STAFF: ['RADIOLOGIST', 'TECHNICIAN'],
  BLOOD_BANK_STAFF: ['BLOOD_BANK_MANAGER', 'DOCTOR', 'NURSE'],
  ALL: Object.values(ROLES)
};

// Vérifie si un utilisateur a un des rôles requis
export const hasRole = (userRoles, requiredRoles) => {
  if (!userRoles) return false;
  if (!Array.isArray(requiredRoles)) requiredRoles = [requiredRoles];
  return userRoles.some(role => requiredRoles.includes(role));
};

// Vérifie si un utilisateur a un des groupes de rôles requis
export const hasRoleGroup = (userRoles, requiredGroups) => {
  if (!userRoles) return false;
  if (!Array.isArray(requiredGroups)) requiredGroups = [requiredGroups];
  
  return requiredGroups.some(group => {
    const groupRoles = ROLE_GROUPS[group] || [];
    return userRoles.some(role => groupRoles.includes(role));
  });
};
