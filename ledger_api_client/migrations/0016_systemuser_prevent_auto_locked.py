# Generated by Django 5.0.8 on 2024-11-07 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger_api_client', '0015_alter_systemuser_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemuser',
            name='prevent_auto_locked',
            field=models.BooleanField(default=False, help_text='Will prevent to auto locking script from locking the account.'),
        ),
    ]
