class PatientsRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'patients':
            # Lire depuis la base régionale
            return 'regionale'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'patients':
            # Écrire dans la base régionale
            return 'regionale'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'patients':
            return db == 'regionale'
        return None
