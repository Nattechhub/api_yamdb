from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    """
    Команда для загрузки данных из файлов csv.
    Передается необязательный параметр path
    с расположением папки с файламми для загрузки.
    Если параметр не задан, берется значение по умолчанию.
    """
    help = 'Import CSV files to SQlite3'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            help=u'Путь до папки с файлами CSV.'
        )

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        if path:
            filepath = path
        else:
            filepath = './static/data/'

        os.system(f'python ./core/import_script.py {filepath}')
