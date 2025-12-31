from django.contrib.auth.models import Permission


def get_all_perms():

    target_models =['sale', 'supplier', 'delivery', 'product', 'transfer', 'branch', 'customer']
    perms_list = list()

    for target_model in target_models:

        model_perms = Permission.objects.filter(content_type__model=target_model)

        perms_list.append({target_model: model_perms})

    return perms_list


def selected_perms(form_data=None):

    perms_selected = list()

    for key, value in form_data.items():
        if key != 'csrfmiddlewaretoken':
            perms_selected.append(key)

    return perms_selected
