"""
Консольная команда для тестирования работы с Gemini API
"""
import json
from django.core.management.base import BaseCommand
from api.services.gemini_service import analyze_school_need, load_scenario_data

class Command(BaseCommand):
    help = 'Тестирование работы с Gemini API для анализа необходимости школ'

    def add_arguments(self, parser):
        parser.add_argument(
            'scenario_id',
            type=int,
            choices=[1, 2, 3],
            help='ID сценария для анализа (1, 2 или 3)'
        )

    def handle(self, *args, **options):
        scenario_id = options['scenario_id']
        
        self.stdout.write(self.style.SUCCESS(f'Тестирование Gemini API с использованием сценария {scenario_id}'))
        
        # Загружаем данные сценария
        scenario_data = load_scenario_data(scenario_id)
        
        if not scenario_data:
            self.stdout.write(self.style.ERROR(f'Сценарий с ID {scenario_id} не найден'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Загружены данные для района: {scenario_data["district_info"]["name"]}'))
        
        # Отправляем запрос в Gemini API
        self.stdout.write('Отправка запроса в Gemini API...')
        result = analyze_school_need(scenario_data)
        
        # Выводим результат
        self.stdout.write(self.style.SUCCESS('Получен ответ от Gemini API:'))
        self.stdout.write('\n' + result + '\n') 