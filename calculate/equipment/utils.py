from django.apps import apps

def get_records_by_supplier(supplier_id, model_names):
    """
    Универсальная функция для получения всех записей, связанных с поставщиком.
    """
    records = {}
    for model_name in model_names:
        try:
            # Получение модели по имени
            model = apps.get_model(model_name)

            # Проверка наличия поля 'supplier'
            if hasattr(model, 'supplier'):
                # Фильтрация записей по поставщику
                supplier_records = model.objects.filter(supplier_id=supplier_id)
                
                # Если есть записи, сохраняем их
                records[model._meta.verbose_name_plural] = supplier_records
            else:
                # Модель не имеет поля 'supplier'
                records[model_name] = f"Model '{model_name}' does not have a 'supplier' field."
        except LookupError as e:
            # Ошибка при получении модели
            records[model_name] = f"Model '{model_name}' not found. Error: {e}"
    return records
