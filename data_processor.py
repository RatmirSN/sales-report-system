"""
Модуль для обработки данных о выполнении плана подключения новых абонентов
"""

import pandas as pd
from typing import List, Dict, Any


class DataProcessor:
    """Класс для обработки данных о продажах"""
    
    def __init__(self):
        self.employees_data = []
        self.plan_data = []
        self.fact_data = []
        self.applications_data = []
    
    def load_employees(self, employees: List[Dict[str, Any]]) -> None:
        """Загрузка данных о сотрудниках"""
        self.employees_data = employees
    
    def load_plan(self, plan_data: List[Dict[str, Any]]) -> None:
        """Загрузка данных о доведенном плане"""
        self.plan_data = plan_data
    
    def load_fact(self, fact_data: List[Dict[str, Any]]) -> None:
        """Загрузка данных о фактическом выполнении"""
        self.fact_data = fact_data
    
    def load_applications(self, applications_data: List[Dict[str, Any]]) -> None:
        """Загрузка данных о заявках в работе"""
        self.applications_data = applications_data
    
    def process_data(self) -> pd.DataFrame:
        """Объединение и обработка всех данных"""
        
        # Создаем DataFrame для сотрудников
        employees_df = pd.DataFrame(self.employees_data)
        
        # Создаем DataFrame для плана
        plan_df = pd.DataFrame(self.plan_data)
        
        # Создаем DataFrame для факта
        fact_df = pd.DataFrame(self.fact_data)
        
        # Создаем DataFrame для заявок
        applications_df = pd.DataFrame(self.applications_data)
        
        # Объединяем данные
        result = employees_df.copy()
        
        # Добавляем план
        if not plan_df.empty:
            plan_pivot = plan_df.pivot_table(
                index='employee_id', 
                columns='period', 
                values='plan_value', 
                aggfunc='sum'
            ).reset_index()
            result = result.merge(plan_pivot, on='employee_id', how='left')
        
        # Добавляем факт
        if not fact_df.empty:
            fact_pivot = fact_df.pivot_table(
                index='employee_id', 
                columns='period', 
                values='fact_value', 
                aggfunc='sum'
            ).reset_index()
            result = result.merge(fact_pivot, on='employee_id', how='left')
        
        # Добавляем количество заявок в работе
        if not applications_df.empty:
            apps_count = applications_df.groupby('employee_id').size().reset_index(name='applications_in_work')
            result = result.merge(apps_count, on='employee_id', how='left')
            result['applications_in_work'] = result['applications_in_work'].fillna(0).astype(int)
        
        return result
    
    def calculate_performance(self, df: pd.DataFrame, period: str) -> pd.DataFrame:
        """Расчет выполнения плана за указанный период"""
        
        plan_col = period
        fact_col = period
        
        if plan_col not in df.columns or fact_col not in df.columns:
            return df
        
        # Рассчитываем выполнение плана в процентах
        df['performance_percent'] = (df[fact_col] / df[plan_col] * 100).round(2)
        df['performance_percent'] = df['performance_percent'].fillna(0)
        
        # Рассчитываем отклонение от плана
        df['deviation'] = df[fact_col] - df[plan_col]
        df['deviation'] = df['deviation'].fillna(0)
        
        # Определяем статус выполнения
        df['status'] = df['performance_percent'].apply(
            lambda x: 'Выполнен' if x >= 100 else 
                     'В процессе' if x >= 50 else 
                     'Критично'
        )
        
        return df
