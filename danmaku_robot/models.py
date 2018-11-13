import sys

from django.db import models
from django.core.exceptions import ValidationError


class RobotSettings(models.Model):
    name = models.CharField(verbose_name='name', max_length=32, unique=True)
    value = models.CharField(verbose_name='value', max_length=1024)
    type = models.CharField(
        verbose_name='type', max_length=32,
        choices=[
            ('str', 'String'),
            ('int', 'Integer'),
            ('float', 'Float'),
            ('bool', 'Boolean')
        ]
    )

    def save(self, *args, **kwargs):
        self.validate_value()
        return super(RobotSettings, self).save(*args, **kwargs)

    def validate_value(self):
        try:
            __builtins__[self.type](self.value)
        except ValueError:
            raise ValidationError(
                'Value type error',
                code='invalid',
            )

    @property
    def clean_value(self):
        try:
            value = __builtins__[self.type](self.value)
        except ValueError:
            value = None
        return value

    @classmethod
    def get_setting_value(cls, name):
        try:
            value = cls.objects.get(name=name).clean_value
        except cls.DoesNotExist:
            value = None

        return value

    @classmethod
    def set_setting_value(cls, name, value, default_type):
        setting, created = cls.objects.get_or_create(name=name)
        if created:
            setting.value, setting.type = value, default_type
        setting.save()
