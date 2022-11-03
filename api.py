import ast
import json
import requests


class Api:
    '''
    Класс умеет запрашивать у http api информацию о регионах России, форматировать эту информацию в вид [{'region_name': 'region_iso'},] и записывать информацию.
    Пути для записи информации заданы в конструкторе класса.
    '''

    def __init__(self, format: str, api_key: str, balanse: int):
        self.api_key = api_key

        self.cities_request_url = 'http://htmlweb.ru/geo/api.php?area={region_num}&json&api_key={api_key}'
        self.regions_request_url = 'http://htmlweb.ru/geo/api.php?country=ru&json&api_key={api_key}&perpage=89'

        self.cities_source = 'sources/cities_list.txt'
        self.regions_source = 'sources/regions_list.txt'

        self.cities_results = 'results/cities_list.txt'
        self.regions_results = 'results/regions_list.txt'

        self.format = format
        self.balanse = balanse

    def writer(self, path: str, data):
        '''
        Метод записывает информацию. path - путь для записи (см. конструктор), data - информация для записи.
        '''
        with open(
            path, 'w', encoding='utf-8'
        ) as file:
            file.write(str(data))

    def reader(self, path: str) -> dict:
        '''
        Метод читает информацию и переводит её в выражения python (Например, из <str> в <dict>). path - путь для чтения.
        '''
        with open(
            path, 'r', encoding='utf-8'
        ) as file:
            return ast.literal_eval(file.read())

    def format_regions_dict(self, dict: dict) -> list:
        '''
        Метод форматирует исходный словарь регионов и возвращает отформатированный словарь.
        По умолчанию, формат [{'region_name': 'region_iso'},]
        '''
        final_list = []

        for count, values_list in dict.items():
            global region_iso, region_name
            region_name = None
            region_iso = None

            region_dict = {}

            if type(values_list) is not int:
                for key_name, value in values_list.items():
                    if key_name == 'name':
                        region_name = values_list[key_name]

                    elif key_name == 'iso':
                        region_iso = values_list[key_name]

                region_dict[region_name] = region_iso
                final_list.append(region_dict)

        return final_list

    def write_all_regions_sources(self):
        '''
        Метод делает запрос к api и записывает результат в источник регионов (см. путь в конструкторе)
        '''
        response = requests.get(
            self.regions_request_url.format(
                api_key=self.api_key
            )
        )

        response_dict = response.json()

        with open(
            self.regions_source, 'w', encoding='utf-8'
        ) as file:
            file.write(str(response_dict))

        return response_dict

    def write_all_regions(self):
        '''
        Метод последовательно выпоняет след. методы:
        1) write_all_regions_sources
        2) reader
        3) format_regions_dict
        4) writer
        '''
        if self.balanse >= 5:
            self.write_all_regions_sources()
            source_dict = self.reader(
                self.regions_source
            )
            formated_dict = self.format_regions_dict(
                source_dict
            )
            self.writer(
                self.regions_results, formated_dict
            )

            self.balanse -= 5
            print('Список успешно создан')

        else:
            print('Не достаточно запросов на балансе')
