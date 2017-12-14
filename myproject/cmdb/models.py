from django.db import models
from django.contrib.auth.models import User

NONPROD='NP'
PROD='PR'

ENV_CHOICES=(
        (NONPROD, 'NON-PROD'),
        (PROD, 'PROD'),
    )

class Organization(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=50)

    def member(self):
        return [ ci for ci in self.ci_set.all() ]

    def __str__(self):
        return self.name

class CI(models.Model):
    name = models.CharField(max_length=50)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Datacenter(models.Model):
    name = models.CharField(max_length=50)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    location = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Model(models.Model):
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    env = models.CharField(max_length=50,choices=ENV_CHOICES,default=NONPROD)

    def __str__(self):
        return self.name

class ServerModel(Model):
    pass


class Software(CI):
    version = models.CharField(max_length=50)
    env = models.CharField(max_length=50,choices=ENV_CHOICES,default=NONPROD)
    license = models.CharField(max_length=50,null=True)

class OS(Software):
    pass


class Hypervisor(Software):
    pass

class Server(CI):
    ip = models.CharField(max_length=50)
    mem_G = models.IntegerField()
    local_disk = models.CharField(max_length=50)
    power_status = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    env = models.CharField(max_length=50,choices=ENV_CHOICES,default=NONPROD)

class PhysicalServer(Server):
    datacenter = models.ForeignKey(Datacenter, on_delete=models.CASCADE, null=True)
    rack = models.CharField(max_length=50)
    model = models.ForeignKey(ServerModel, on_delete=models.CASCADE, null=True)
    cpu_type = models.CharField(max_length=50)
    cpu_speed = models.CharField(max_length=50)
    cpu_sockets = models.IntegerField()
    cpu_cores = models.IntegerField()
    ext_disk = models.CharField(max_length=50)
    serial = models.CharField(max_length=50)
    maint_status = models.CharField(max_length=50)
    maint_vendor = models.CharField(max_length=50)
    maint_service_from = models.DateField(auto_now=False, auto_now_add=False)
    maint_service_to = models.DateField(auto_now=False, auto_now_add=False)
    check_date = models.DateField(auto_now=False, auto_now_add=False)
    check_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    power_ports = models.IntegerField()
    lan_ports = models.IntegerField()
    fiber_ports = models.IntegerField()
    fiber_cards = models.IntegerField()
    fiber_card_model = models.CharField(max_length=50)


class NONESXServer(PhysicalServer):
    os = models.ForeignKey(OS, on_delete=models.CASCADE, null=True)

class ESXServer(PhysicalServer):
    hypervisor = models.ForeignKey(Hypervisor, on_delete=models.CASCADE, null=True)

class VirtualServer(Server):
    os = models.ForeignKey(OS, on_delete=models.CASCADE, null=True)
    host = models.ForeignKey(ESXServer, on_delete=models.CASCADE, null=True)
    cpu_num = models.IntegerField()
    hypervisor = models.ForeignKey(Hypervisor, on_delete=models.CASCADE, null=True)


