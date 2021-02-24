# Generated by Django 2.2.19 on 2021-02-24 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inspire_eu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationSchema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=32)),
                ('slug', models.CharField(blank=True, db_index=True, max_length=32)),
                ('link', models.URLField()),
                ('version', models.SmallIntegerField(blank=True, default=0)),
                ('label', models.CharField(max_length=128)),
                ('definition', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Application Schema',
                'verbose_name_plural': 'Application Schemes',
                'ordering': ['code', 'label'],
            },
        ),
        migrations.CreateModel(
            name='CodeList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=64)),
                ('slug', models.CharField(blank=True, db_index=True, max_length=64)),
                ('link', models.URLField(blank=True)),
                ('label', models.CharField(max_length=128)),
                ('definition', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('application_schema', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inspire_eu.ApplicationSchema')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='inspire_eu.CodeList')),
            ],
            options={
                'verbose_name': 'Code list',
                'verbose_name_plural': 'Code lists',
                'ordering': ['code', 'label'],
            },
        ),
        migrations.CreateModel(
            name='Namespace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='Namespace', max_length=32)),
                ('name', models.CharField(blank=True, max_length=64)),
            ],
            options={
                'verbose_name': 'Namespace',
                'verbose_name_plural': 'Namespaces',
                'ordering': ['code', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=32)),
                ('slug', models.CharField(blank=True, db_index=True, max_length=32)),
                ('label', models.CharField(max_length=128)),
                ('definition', models.TextField(blank=True)),
                ('link', models.URLField()),
                ('is_valid', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Status',
                'verbose_name_plural': 'Status',
                'ordering': ['is_valid', 'label'],
            },
        ),
        migrations.CreateModel(
            name='UnitOfMeasure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='The name(s) of a particular unit of measure. Examples would include the following: 1) for uomArea - square feet <br />2) for uomTime - seconds <br />3) for uomArea - miles<br />4) uomAngle - degrees.', max_length=32)),
                ('slug', models.CharField(blank=True, db_index=True, max_length=32)),
                ('symbol', models.CharField(help_text='The symbol used for this unit of measure, such at "ft" for feet, or "m" for meter.', max_length=8)),
                ('measure_type', models.CharField(choices=[('', 'Unknown'), ('area', 'Area'), ('length', 'Length'), ('angle', 'Angle'), ('time', 'Time'), ('velocity', 'Velocity'), ('volume', 'Volume'), ('scale', 'Scale'), ('weight', 'Weight')], help_text='Measure Type', max_length=8)),
                ('name_standard_unit', models.CharField(blank=True, help_text='Name of the standard units to which this unit of measure can be directly converted. If this variable is NULL, then the standard unit for this measure type given by the local copy of the StandardsUnits code list.', max_length=8)),
                ('scale_to_standard_unit', models.FloatField(blank=True, help_text='If the implementation system used for this object does not support NULL, the  scale set to 0 is equivalent to NULL for both scale and offset.<br />If X is the current unit, and S is the standard one the of two variables scale(ToStandardUnit) and offset(ToStandardUnit) can be used to make the conversion from X to S by:<br />S = offset + scale*X <br />and, conversely, <br />X = (S-offset)/scale', null=True)),
                ('offset_to_standard_unit', models.FloatField(blank=True, help_text='See scaleToStandardUnit for a description. Again, this variable is NULL is no linear conversion is possible. If the two units are only a scale in difference, then this number is zero (0). If the implementation system used for this object does not support NULL, the then scale set to 0 is equivalent to NULL for both scale and offset.', null=True)),
                ('formula', models.CharField(blank=True, help_text='An algebraic formula (probably in some programming language) converting this unit of measure (represented in the formula by its uomSymbol) to the ISO standard (represented by its symbol. This member attribute is not required, but it is a valuable piece of documentation. ', max_length=32)),
            ],
            options={
                'verbose_name': 'Unit Of Measure',
                'verbose_name_plural': 'Units Of Measure',
                'ordering': ['symbol', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=32)),
                ('slug', models.CharField(blank=True, db_index=True, max_length=32)),
                ('link', models.URLField()),
                ('version', models.SmallIntegerField(blank=True, default=0)),
                ('label', models.CharField(max_length=128)),
                ('definition', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inspire_eu.Status')),
            ],
            options={
                'verbose_name': 'Theme',
                'verbose_name_plural': 'Themes',
                'ordering': ['code', 'label'],
            },
        ),
        migrations.CreateModel(
            name='CodeListValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(db_index=True, max_length=96)),
                ('slug', models.CharField(blank=True, db_index=True, max_length=96)),
                ('link', models.URLField()),
                ('label', models.CharField(max_length=200)),
                ('definition', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('code_list', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inspire_eu.CodeList')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inspire_eu.Status')),
            ],
            options={
                'verbose_name': 'Code list value',
                'verbose_name_plural': 'Code list values',
                'ordering': ['code_list__code', 'code', 'label'],
            },
        ),
        migrations.AddField(
            model_name='codelist',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inspire_eu.Status'),
        ),
        migrations.AddField(
            model_name='codelist',
            name='themes',
            field=models.ManyToManyField(to='inspire_eu.Theme'),
        ),
        migrations.AddField(
            model_name='applicationschema',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inspire_eu.Status'),
        ),
        migrations.AddField(
            model_name='applicationschema',
            name='themes',
            field=models.ManyToManyField(to='inspire_eu.Theme'),
        ),
    ]
