# Generated by Django 4.2.4 on 2024-08-15 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('direct_messages', '0002_conversation_message_delete_directmessage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['created_at']},
        ),
    ]
