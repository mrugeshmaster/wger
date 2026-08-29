from django.db import migrations

# The trophy that the streak checker awards. Migration 0002 carries the trophy
# data inline, so editing the JSON fixture only changes what the test suite
# loads, not what a running server has.
UNSTOPPABLE_UUID = 'b605b6a1-953d-41fb-87c9-a2f88b5f5907'


def set_streak_type(apps, schema_editor):
    Trophy = apps.get_model('trophies', 'Trophy')
    Trophy.objects.filter(uuid=UNSTOPPABLE_UUID).update(trophy_type='streak')


def restore_sequence_type(apps, schema_editor):
    Trophy = apps.get_model('trophies', 'Trophy')
    Trophy.objects.filter(uuid=UNSTOPPABLE_UUID).update(trophy_type='sequence')


class Migration(migrations.Migration):
    dependencies = [
        ('trophies', '0004_alter_trophy_trophy_type'),
    ]

    operations = [
        migrations.RunPython(set_streak_type, restore_sequence_type),
    ]
