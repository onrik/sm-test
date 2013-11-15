# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from picklefield.fields import PickledObjectField


class Model(models.Model):
    name = models.CharField(max_length=100, unique=True, primary_key=True)
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return self.title

    def get_objects(self):
        return self.modelobject_set.all()

    def as_dict(self):
        return {
            'name': self.name,
            'title': self.title,
        }


class Field(models.Model):
    TYPE_INT = 'int'
    TYPE_CHAR = 'char'
    TYPE_DATE = 'date'

    TYPE_CHOICES = (
        (TYPE_INT, 'Число'),
        (TYPE_CHAR, 'Строка'),
        (TYPE_DATE, 'Дата'),
    )

    model = models.ForeignKey(Model, related_name='fields')
    field_id = models.CharField(max_length=100, verbose_name='Id')
    type = models.CharField(max_length=4, choices=TYPE_CHOICES)
    title = models.CharField(max_length=100)

    class Meta:
        unique_together = ('model', 'field_id')

    def as_dict(self):
        return {
            'type': self.type,
            'field_id': self.field_id,
            'title': self.title
        }

    def form_field(self):
        if self.type == self.TYPE_INT:
            return forms.IntegerField()
        elif self.type == self.TYPE_CHAR:
            return forms.CharField()
        elif self.type == self.TYPE_DATE:
            return forms.DateField(input_formats=('%d.%m.%Y',))


class ModelObject(models.Model):
    model = models.ForeignKey(Model)
    values = PickledObjectField()

    def __getattr__(self, item):
        if hasattr(self, item):
            return super(ModelObject, self).__getattr__(item)
        elif isinstance(self.values, dict) and item in self.values:
            return self.values.get(item)
        else:
            raise AttributeError

    def as_dict(self):
        data = {'id': self.id}
        for field in self.model.fields.all():
            if field.type == field.TYPE_DATE and self.values.get(field.field_id):
                data[field.field_id] = self.values.get(field.field_id).strftime('%d.%m.%Y')
            else:
                data[field.field_id] = self.values.get(field.field_id)

        return data
