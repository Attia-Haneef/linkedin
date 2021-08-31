# Generated by Django 3.2.6 on 2021-08-30 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20210829_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='education',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='education',
            name='member',
        ),
        migrations.RemoveField(
            model_name='education',
            name='start_date',
        ),
        migrations.AlterField(
            model_name='education',
            name='institute',
            field=models.CharField(choices=[('Punjab Clg', 'Punjab Clg'), ('Fast Nuces', 'Fast Nuces')], max_length=50),
        ),
        migrations.AlterField(
            model_name='member',
            name='connections',
            field=models.ManyToManyField(blank=True, related_name='_myapp_member_connections_+', through='myapp.Connection', to='myapp.Member'),
        ),
        migrations.CreateModel(
            name='MemberEducation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('education', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.education')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.member')),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='educations',
            field=models.ManyToManyField(blank=True, through='myapp.MemberEducation', to='myapp.Education'),
        ),
    ]
