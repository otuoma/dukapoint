def delivery_value(products_list):

    del_val = 0

    for item in products_list:

        del_val += item['total_cost']

    return del_val

