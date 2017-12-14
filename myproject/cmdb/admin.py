from django.contrib import admin
from .models import *

# single

class DatacenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ['name']

admin.site.register(Datacenter, DatacenterAdmin)

class CIInline(admin.StackedInline):
    model = CI
    extra = 0
    fields=('name',)

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name','member')
    inlines = [CIInline]

admin.site.register(Group, GroupAdmin)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

admin.site.register(Organization, OrganizationAdmin)


class OSAdmin(admin.ModelAdmin):
    list_display = ('name', 'org','version','env','license','group')

admin.site.register(OS, OSAdmin)


class HypervisorAdmin(admin.ModelAdmin):
    list_display = ('name', 'org','version','env','license','group')

admin.site.register(Hypervisor, HypervisorAdmin)


class ServerModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'org','brand','env')

admin.site.register(ServerModel, ServerModelAdmin)

class NONESXServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'org','mem_G','env','power_status','serial','datacenter','cpu_sockets','cpu_cores','rack','model','os')

admin.site.register(NONESXServer, NONESXServerAdmin)

class ESXServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'org','mem_G','env','power_status','serial','datacenter','cpu_sockets','cpu_cores','rack','model','hypervisor')

admin.site.register(ESXServer, ESXServerAdmin)

class VirtualServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'org','mem_G','env','power_status','cpu_num','os','host','hypervisor')

admin.site.register(VirtualServer, VirtualServerAdmin)

class PhysicalServerAdmin(admin.ModelAdmin):
    list_display = ('name', 'org','mem_G','env','power_status','serial','datacenter','cpu_sockets','cpu_cores','rack','model')

admin.site.register(PhysicalServer, PhysicalServerAdmin)