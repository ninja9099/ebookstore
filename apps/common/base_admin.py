from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ()

    def get_readonly_fields(self, request, obj=None):
        audit_fields = ['created_by', 'updated_by', 'created_ts', 'updated_ts']
        return set(list(self.readonly_fields) + audit_fields)

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
        obj.save()
