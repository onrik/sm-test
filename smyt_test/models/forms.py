import yaml

from django import forms

from .models import Model, Field


class ModelObjectForm(forms.Form):
    def __init__(self, model, **kwargs):
        super(ModelObjectForm, self).__init__(**kwargs)
        for field in model.fields.all():
            self.fields[field.field_id] = field.form_field()


class CreateModelsForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        f = self.cleaned_data['file']
        data = yaml.load(f.read())
        if not isinstance(data, dict):
            raise forms.ValidationError('Wrong file format')
        return data

    def save(self, data):
        for name in data:
            model = Model()
            model.name = name
            model.title = data[name]['title']
            model.save()
            for field in data[name]['fields']:
                Field.objects.create(
                    model=model,
                    field_id=field['id'],
                    type=field['type'],
                    title=field['title'],
                )