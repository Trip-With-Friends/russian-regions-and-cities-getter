def write_results(format: str, type_of_places: str, data: list):
    '''
    format. Например: 'js', 'py' (Формат файла)
    type_of_places. Например: 'cities', 'regions' (Тип места)
    data. Например: [{'MSK':['Москва']}] (Данные для записи)
    '''
    cities_path_template = '{format}_sources/cities_list.{format}'
    regions_path_template = '{format}_sources/regions_list.{format}'

    if type_of_places == 'cities':
        file_path = cities_path_template.format(format=format)

        with open(file_path, 'w') as file:
            file.write(str(data))

    elif type_of_places == 'regions':
        file_path = regions_path_template.format(format=format)

        with open(file_path, 'w') as file:
            file.write(str(data))
