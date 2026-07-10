"""
Модуль для генерации отчета по выполнению плана подключения новых абонентов
"""

import pandas as pd
from datetime import datetime
from typing import Optional
import os


class ReportGenerator:
    """Класс для генерации отчетов"""
    
    def __init__(self, data_processor):
        self.data_processor = data_processor
        self.report_data = None
    
    def generate_report(self, period: str = 'current_month') -> pd.DataFrame:
        """Генерация отчета за указанный период"""
        
        # Обрабатываем данные
        df = self.data_processor.process_data()
        
        # Рассчитываем выполнение плана
        df = self.data_processor.calculate_performance(df, period)
        
        self.report_data = df
        return df
    
    def format_report(self, df: pd.DataFrame) -> pd.DataFrame:
        """Форматирование отчета для отображения"""
        
        # Выбираем нужные колонки для отчета
        columns_to_show = [
            'employee_name', 'department', 'position',
            period, f'{period}_y', 'applications_in_work',
            'performance_percent', 'deviation', 'status'
        ]
        
        # Переименовываем колонки для читаемости
        column_mapping = {
            'employee_name': 'Сотрудник',
            'department': 'Отдел',
            'position': 'Должность',
            period: 'План',
            f'{period}_y': 'Факт',
            'applications_in_work': 'Заявок в работе',
            'performance_percent': 'Выполнение %',
            'deviation': 'Отклонение',
            'status': 'Статус'
        }
        
        # Проверяем наличие колонок
        available_columns = [col for col in columns_to_show if col in df.columns]
        
        report_df = df[available_columns].copy()
        report_df = report_df.rename(columns=column_mapping)
        
        # Форматируем числовые значения
        if 'План' in report_df.columns:
            report_df['План'] = report_df['План'].fillna(0).astype(int)
        if 'Факт' in report_df.columns:
            report_df['Факт'] = report_df['Факт'].fillna(0).astype(int)
        if 'Выполнение %' in report_df.columns:
            report_df['Выполнение %'] = report_df['Выполнение %'].round(2)
        if 'Отклонение' in report_df.columns:
            report_df['Отклонение'] = report_df['Отклонение'].astype(int)
        
        return report_df
    
    def export_to_excel(self, df: pd.DataFrame, filename: Optional[str] = None) -> str:
        """Экспорт отчета в Excel"""
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'sales_report_{timestamp}.xlsx'
        
        filepath = os.path.join(os.getcwd(), filename)
        
        # Создаем Excel writer с форматированием
        with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Отчет', index=False)
            
            # Получаем workbook и worksheet
            workbook = writer.book
            worksheet = writer.sheets['Отчет']
            
            # Определяем форматы
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4472C4',
                'font_color': 'white',
                'border': 1,
                'align': 'center',
                'valign': 'vcenter'
            })
            
            number_format = workbook.add_format({'num_format': '#,##0'})
            percent_format = workbook.add_format({'num_format': '0.00'})
            
            # Применяем форматирование к заголовкам
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
                worksheet.set_column(col_num, col_num, 15)
            
            # Применяем форматирование к числовым колонкам
            for row_num in range(1, len(df) + 1):
                if 'План' in df.columns:
                    worksheet.write(row_num, df.columns.get_loc('План'), 
                                  df.iloc[row_num-1]['План'], number_format)
                if 'Факт' in df.columns:
                    worksheet.write(row_num, df.columns.get_loc('Факт'), 
                                  df.iloc[row_num-1]['Факт'], number_format)
                if 'Выполнение %' in df.columns:
                    worksheet.write(row_num, df.columns.get_loc('Выполнение %'), 
                                  df.iloc[row_num-1]['Выполнение %'], percent_format)
            
            # Добавляем условное форматирование для статуса
            if 'Статус' in df.columns:
                worksheet.conditional_format(
                    1, df.columns.get_loc('Статус'),
                    len(df), df.columns.get_loc('Статус'),
                    {
                        'type': 'text',
                        'criteria': 'containing',
                        'value': 'Выполнен',
                        'format': workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
                    }
                )
                worksheet.conditional_format(
                    1, df.columns.get_loc('Статус'),
                    len(df), df.columns.get_loc('Статус'),
                    {
                        'type': 'text',
                        'criteria': 'containing',
                        'value': 'В процессе',
                        'format': workbook.add_format({'bg_color': '#FFEB9C', 'font_color': '#9C5700'})
                    }
                )
                worksheet.conditional_format(
                    1, df.columns.get_loc('Статус'),
                    len(df), df.columns.get_loc('Статус'),
                    {
                        'type': 'text',
                        'criteria': 'containing',
                        'value': 'Критично',
                        'format': workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
                    }
                )
        
        return filepath
    
    def get_summary(self, df: pd.DataFrame) -> Dict:
        """Получение сводной информации по отчету"""
        
        summary = {
            'total_employees': len(df),
            'total_plan': df['План'].sum() if 'План' in df.columns else 0,
            'total_fact': df['Факт'].sum() if 'Факт' in df.columns else 0,
            'total_applications': df['Заявок в работе'].sum() if 'Заявок в работе' in df.columns else 0,
            'avg_performance': df['Выполнение %'].mean() if 'Выполнение %' in df.columns else 0,
            'completed_count': len(df[df['Статус'] == 'Выполнен']) if 'Статус' in df.columns else 0,
            'in_progress_count': len(df[df['Статус'] == 'В процессе']) if 'Статус' in df.columns else 0,
            'critical_count': len(df[df['Статус'] == 'Критично']) if 'Статус' in df.columns else 0
        }
        
        return summary
