function create_object(button){
    var fields = $(button).parents('tr').find('input');
    var data = {};
    for (var i=0; i<fields.length; i++){
        data[fields[i].name] = fields[i].value;
    }
    $.post('/create/', data, function(response){
        console.log(response);
        if (response.status == 'ok'){
            var new_form = $('#new-object-form').clone();
            new_form.find('input').val('');

            console.log(response);
            var form = $('#new-object-form');
            var cells = form.find('td');
            $(cells[0]).text(response.id);
            for (var i=1; i<cells.length; i++){
                var cell = $(cells[i]);
                cell.text(cell.find('input')[0].value);
            }

            form.attr('id', '');
            var table = $('#objects-table').find('tbody').get(0);
            $(table).append(new_form);
        }
        else {
            $('#new-object-form').find('.error').empty();
            for (var field in response.errors){
                $('#new-object-form').find('#' + field + '_error').text(response.errors[field]);
            }
        }
    });
}

function edit_field(field){
    var text = $(field).text().trim();
    $(field).width($(field).width());
    $(field).html($('#input-template').render({'value': text, 'witdh': $(field).width()}));
}

function edit_finished(button, save){
    var field = $(button).parents('.input-group').find('input');
//    field.data('current-value');
    var cell = $(button).parent();
    cell.empty();
//    $(cell).text('');
//    cell.text(field.data('old-value'));

}

function get_objects(link, model_name){
    $('#models-list').find('a').removeClass('active');
    $(link).addClass('active');

    var table = $('#objects-table');
    table.empty();

    $.getJSON('/objects/' + model_name + '/', function(response){
        table.append($('#table-head-template').render({'fields': response.fields}));
        var tbody = $('<tbody></tbody>');
        for (var i=0; i<response.objects.length; i++){
            var context = {
                'fields': response.fields,
                'object': response.objects[i]
            };
            tbody.append($('#object-template').render(context));
        }
        tbody.append($('#form-template').render({'fields': response.fields, 'model': response.model}));
        table.append(tbody);
    });
}