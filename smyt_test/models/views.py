from django.core.serializers.json import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Model, ModelObject
from .forms import ModelObjectForm, CreateModelsForm


def get_objects_view(request, model_name):
    model = get_object_or_404(Model, name=model_name)
    response = {
        'model': model.as_dict(),
        'fields': [field.as_dict() for field in model.fields.all()],
        'objects': [obj.as_dict() for obj in model.get_objects()],
    }

    return HttpResponse(json.dumps(response), content_type='application/json')


@csrf_exempt
@require_POST
def create_object_view(request):
    model = get_object_or_404(Model, name=request.POST.get('model'))
    form = ModelObjectForm(data=request.POST, model=model)
    if form.is_valid():
        obj = ModelObject()
        obj.model = model
        obj.values = form.cleaned_data
        obj.save()
        response = {
            'status': 'ok',
            'id': obj.id,
        }
    else:
        response = {
            'status': 'error',
            'errors': {field: error[0] for field, error in form.errors.items()}
        }

    return HttpResponse(json.dumps(response), content_type='application/json')


def create_models_view(request):
    form = CreateModelsForm(request.POST, request.FILES)

    if form.is_valid():
        form.save(form.cleaned_data['file'])

    return HttpResponseRedirect('/')


def index(request):
    models = Model.objects.all()
    context = {
        'models': models,
        'model': models[0] if models else None,

    }
    return render(request, 'base.html', context)