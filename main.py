"""
Основной модуль для запуска системы отчетности по выполнению плана подключения новых абонентов
"""

from data_processor import DataProcessor
from report_generator import ReportGenerator
import json


def load_example_data():
    """Загрузка примера данных"""
    
    # Данные о сотрудниках
    employees = [
        {'employee_id': 1, 'employee_name': 'Иванов И.И.', 'department': 'Отдел продаж', 'position': 'Менеджер'},
        {'employee_id': 2, 'employee_name': 'Петров П.П.', 'department': 'Отдел продаж', 'position': 'Старший менеджер'},
        {'employee_id': 3, 'employee_name': 'Сидоров С.С.', 'department': 'Отдел продаж', 'position': 'Менеджер'},
        {'employee_id': 4, 'employee_name': 'Козлов К.К.', 'department': 'Отдел продаж', 'position': 'Менеджер'},
        {'employee_id': 5, 'employee_name': 'Николаев Н.Н.', 'department': 'Отдел продаж', 'position': 'Менеджер'},
    ]
    
    # Данные о доведенном плане
    plan_data = [
        {'employee_id': 1, 'period': 'current_month', 'plan_value': 50},
        {'employee_id': 2, 'period': 'current_month', 'plan_value': 60},
        {'employee_id': 3, 'period': 'current_month', 'plan_value': 45},
        {'employee_id': 4, 'period': 'current_month', 'plan_value': 55},
        {'employee_id': 5, 'period': 'current_month', 'plan_value': 40},
    ]
    
    # Данные о фактическом выполнении
    fact_data = [
        {'employee_id': 1, 'period': 'current_month', 'fact_value': 52},
        {'employee_id': 2, 'period': 'current_month', 'fact_value': 58},
        {'employee_id': 3, 'period': 'current_month', 'fact_value': 30},
        {'employee_id': 4, 'period': 'current_month', 'fact_value': 55},
        {'employee_id': 5, 'period': 'current_month', 'fact_value': 35},
    ]
    
    # Данные о заявках в работе
    applications_data = [
        {'employee_id': 1, 'application_id': 101, 'status': 'in_progress'},
        {'employee_id': 1, 'application_id': 102, 'status': 'in_progress'},
        {'employee_id': 1, 'application_id': 103, 'status': 'in_progress'},
        {'employee_id': 2, 'application_id': 201, 'status': 'in_progress'},
        {'employee_id': 2, 'application_id': 202, 'status': 'in_progress'},
        {'employee_id': 3, 'application_id': 301, 'status': 'in_progress'},
        {'employee_id': 3, 'application_id': 302, 'status': 'in_progress'},
        {'employee_id': 3, 'application_id': 303, 'status': 'in_progress'},
        {'employee_id': 3, 'application_id': 304, 'status': 'in_progress'},
        {'employee_id': 4, 'application_id': 401, 'status': 'in_progress'},
        {'employee_id': 5, 'application_id': 501, 'status': 'in_progress'},
        {'employee_id': 5, 'application_id': 502, 'status': 'in_progress'},
    ]
    
    return employees, plan_data, fact_data, applications_data


def main():
    """Главная функция"""
    
    print("=== Система отчетности по выполнению плана подключения новых абонентов ===\n")
    
    # Инициализация процессора данных
    processor = DataProcessor()
    
    # Загрузка данных
    print("Загрузка данных...")
    employees, plan_data, fact_data, applications_data = load_example_data()
    
    processor.load_employees(employees)
    processor.load_plan(plan_data)
    processor.load_fact(fact_data)
    processor.load_applications(applications_data)
    
    # Инициализация генератора отчетов
    generator = ReportGenerator(processor)
    
    # Генерация отчета
    print("Генерация отчета...")
    period = 'current_month'
    report_df = generator.generate_report(period)
    
    # Форматирование отчета
    formatted_report = generator.format_report(report_df)
    
    # Вывод отчета в консоль
    print("\n" + "="*100)
    print("ОТЧЕТ ПО ВЫПОЛНЕНИЮ ПЛАНА ПОДКЛЮЧЕНИЯ НОВЫХ АБОНЕНТОВ")
    print("="*100)
    print(formatted_report.to_string(index=False))
    print("="*100)
    
    # Вывод сводной информации
    summary = generator.get_summary(formatted_report)
    print("\nСВОДНАЯ ИНФОРМАЦИЯ:")
    print(f"- Всего сотрудников: {summary['total_employees']}")
    print(f"- Общий план: {summary['total_plan']}")
    print(f"- Общий факт: {summary['total_fact']}")
    print(f"- Всего заявок в работе: {summary['total_applications']}")
    print(f"- Среднее выполнение плана: {summary['avg_performance']:.2f}%")
    print(f"- Выполнили план: {summary['completed_count']}")
    print(f"- В процессе выполнения: {summary['in_progress_count']}")
    print(f"- Критичное отставание: {summary['critical_count']}")
    
    # Экспорт в Excel
    print("\nЭкспорт отчета в Excel...")
    filepath = generator.export_to_excel(formatted_report)
    print(f"Отчет сохранен: {filepath}")
    
    print("\nГотово!")


if __name__ == "__main__":
    main()
