from django.contrib import admin
from django.db import IntegrityError
from import_export.admin import ImportExportModelAdmin

from v1.models.devices import Device
from v1.models.home import Report, ClientIABSAccount
from v1.models.documents import Document_type, PurposeCode, MFO
from django.contrib.auth.models import Permission as DjangoPermission
from v1.models.users import Role, Permission, RolePermission, Users, AccessToken
from v1.models import News, Notifications, DocHistories, DocumentRegistration, ClientInfo, Sample, BudgetIncomeAccount, \
    BudgetAccount, Identification, ClientCertificate
from v1.models.transaction import DocTest

from import_export import resources


class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'role', 'permission']


class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'expense_article', 'client']


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'company_name', 'mfo', 'inn', 'code', 'director', 'accountant']


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'user', 'role']

    def user_id(self, obj):
        return obj.user.id


class BudgetAccountResource(resources.ModelResource):
    class Meta:
        model = BudgetAccount
        import_id_fields = ('code',)

    def import_data(self, dataset, **kwargs):
        objs = []
        errors = []
        for row in dataset.dict:
            print("Row:", row)  # Log each row for debugging
            # Ensure required fields are present
            if not all(row.get(field) for field in ['code', 'name', 'tin']):
                errors.append(f"Missing required fields in row: {row}")
                continue

            # Create the object excluding the 'id' field
            objs.append(BudgetAccount(
                code=row['code'],
                name=row['name'],
                tin=row['tin'],
            ))

        try:
            BudgetAccount.objects.bulk_create(objs)
        except IntegrityError as e:
            errors.append(f"Integrity error: {e}")

        if errors:
            for error in errors:
                print(error)


class BudgetAccountAdmin(ImportExportModelAdmin):
    resource_class = BudgetAccountResource
    list_display = ('code', 'name', 'tin')


class BudgetIncomeAccountResource(resources.ModelResource):
    class Meta:
        model = BudgetIncomeAccount
        import_id_fields = ('code',)

    def import_data(self, dataset, **kwargs):
        objs = []
        errors = []
        for row in dataset.dict:
            # Ensure required fields are present
            if not all(row.get(field) for field in ['code', 'name', 'coato', 'region_code']):
                errors.append(f"Missing required fields in row: {row}")
                continue

            # Create the object excluding the 'id' field
            objs.append(BudgetIncomeAccount(
                code=row['code'],
                name=row['name'],
                coato=row['coato'],
                region_code=row['region_code'],
            ))

        try:
            BudgetIncomeAccount.objects.bulk_create(objs)
        except IntegrityError as e:
            errors.append(f"Integrity error: {e}")

        if errors:
            for error in errors:
                print(error)


class BudgetIncomeAccountAdmin(ImportExportModelAdmin):
    resource_class = BudgetIncomeAccountResource
    list_display = ('code', 'name', 'coato', 'region_code')


admin.site.register(DocHistories)
admin.site.register(Role, RoleAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(RolePermission, RolePermissionAdmin)
admin.site.register(DjangoPermission)
admin.site.register(Report, ReportAdmin)
admin.site.register(MFO)
admin.site.register(Device)
admin.site.register(News)
admin.site.register(Notifications)
admin.site.register(PurposeCode)
admin.site.register(Document_type)
admin.site.register(Users)
admin.site.register(DocumentRegistration)
admin.site.register(ClientInfo)
admin.site.register(ClientIABSAccount)
admin.site.register(AccessToken)
admin.site.register(Sample)
admin.site.register(BudgetIncomeAccount, BudgetIncomeAccountAdmin)
admin.site.register(BudgetAccount, BudgetAccountAdmin)
admin.site.register(DocTest)
admin.site.register(Identification)
admin.site.register(ClientCertificate)
