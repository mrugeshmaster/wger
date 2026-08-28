from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('weight', '0005_add_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='weightentry',
            name='notes',
            field=models.CharField(
                blank=True,
                default='',
                help_text='Anything worth remembering about this entry, e.g. "after holidays"',
                max_length=100,
                verbose_name='Notes',
            ),
        ),
    ]
