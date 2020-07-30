# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Data(models.Model):
    id = models.AutoField(primary_key=True)
    # null默认False，非空
    text = models.TextField(blank=True, null=True, verbose_name='段子')

    class Meta:
        managed = False
        db_table = 'data'
