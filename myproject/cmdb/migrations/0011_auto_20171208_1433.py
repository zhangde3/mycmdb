# Generated by Django 2.0 on 2017-12-08 06:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cmdb', '0010_auto_20171208_1432'),
    ]

    operations = [
        migrations.CreateModel(
            name='Datacenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='datacenter',
            name='group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cmdb_datacenter_related', related_query_name='cmdb_datacenters', to='cmdb.Group'),
        ),
        migrations.AddField(
            model_name='datacenter',
            name='org',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cmdb_datacenter_related', related_query_name='cmdb_datacenters', to='cmdb.Organization'),
        ),
    ]
