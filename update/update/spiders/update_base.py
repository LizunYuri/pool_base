import re
import scrapy
import json
from datetime import datetime
import requests
import os
from scrapy.spidermiddlewares.httperror import HttpError


base_url = 'http://localhost:8000/'


class BaseUpdateSpider(scrapy.Spider):
    """Базовый класс для обновления данных о товарах."""

    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
        'ROBOTSTXT_OBEY': False,  # Отключаем проверку robots.txt
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.offsite.OffsiteMiddleware': None,
            'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,  # Включаем HttpErrorMiddleware
        },
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }

    def __init__(self, endpoint, *args, **kwargs):
        super(BaseUpdateSpider, self).__init__(*args, **kwargs)
        self.endpoint = endpoint
        self.products = []  # Инициализация списка для хранения всех товаров
        self.messages = []  # Список для хранения сообщений для отправки в Django

    def parse(self, response):
        """Парсит данные с заданного URL."""
        data = json.loads(response.body)

        for item in data:
            supplier = item.get('supplier', {})
            product_info = self.create_product_info(item, supplier)

            self.products.append(product_info)

            product_url = item.get('url')
            if product_url:
                yield scrapy.Request(url=product_url, callback=self.parse_product_page, errback=self.handle_error, meta={'product_key': product_info['id']})
            else:
                self.handle_missing_product_url(product_info)

    def create_product_info(self, item, supplier):
        """Создает словарь с информацией о товаре."""
        return {
            'id': item['id'],
            'name': item['name'],
            'url': item.get('url'),
            'supplier_id': supplier.get('id'),
            'supplier_name': supplier.get('name'),
            'supplier_url': supplier.get('url'),
            'price': item.get('price', None),
            'date': item.get('date', None),
            'status': 'not_found'  # Статус по умолчанию
        }

    def handle_missing_product_url(self, product_info):
        """Обрабатывает случай, когда отсутствует product_url."""
        message = {
            'product_id': product_info['id'],
            'product_name': product_info['name'],
            'message': 'product_url отсутствует, цена не обновлена.',
            'timestamp': datetime.now().isoformat()  # Добавляем временную метку
        }
        self.messages.append(message)  # Сохраняем сообщение в список
        self.log(f"Сообщение добавлено: {message}")

    def parse_product_page(self, response):
        """Парсит страницу товара для получения цены."""
        product_key = response.meta['product_key']
        item = next((prod for prod in self.products if prod['id'] == product_key), None)

        if response.status // 100 == 3:  # Обрабатываем ошибки 3xx
            self.log(f"Перенаправление на {response.url}, статус: {response.status}")

        if item:
            matched_elements = response.xpath("//*[contains(@class, 'price') or contains(@id, 'price')]").getall()
            price_found = False

            if not matched_elements:
                self.log(f"Нет элементов с ценой для товара '{item['name']}' на странице.")

            for element in matched_elements:
                price_match = re.search(r'(\d{1,3}(?:[\s.,]?\d{3})*(?:[\.,]\d{0,2})?)\s*(₽|руб|RUB|р)', element)

                if price_match:
                    price_str = price_match.group(1).replace(' ', '').replace('\u00A0', '').replace(',', '.')
                    try:
                        new_price = float(price_str)
                        self.update_price(item, new_price)
                        price_found = True
                        break  # Прекращаем поиск после нахождения цены
                    except ValueError:
                        self.log(f"Не удалось преобразовать цену: {price_str}")
                        item['price'] = None

            if not price_found:
                self.log(f"Цена для товара '{item['name']}' не найдена.")
                message = {
                    'product_id': item['id'],
                    'product_name': item['name'],
                    'message': 'Цена для товара не найдена.',
                    'timestamp': datetime.now().isoformat()  # Добавляем временную метку
                }
                self.messages.append(message)  # Сохраняем сообщение в список
                self.log(f"Сообщение добавлено: {message}")  # Логируем добавление сообщения
        else:
            self.log(f"Ошибка: товар с ID {product_key} не найден в списке.")

    def handle_error(self, failure):
        """Обрабатывает ошибки запросов, такие как 404."""
        if failure.check(HttpError):
            response = failure.value.response
            if response.status == 404:
                product_key = failure.request.meta.get('product_key')
                item = next((prod for prod in self.products if prod['id'] == product_key), None)

                if item:
                    message = {
                        'product_id': item['id'],
                        'product_name': item['name'],
                        'message': f'Ошибка 404: Страница не найдена для {response.url}',
                        'timestamp': datetime.now().isoformat()
                    }
                    self.messages.append(message)
                    self.log(f"Сообщение добавлено: {message}")
                else:
                    self.log(f"Ошибка: товар с ID {product_key} не найден в списке.")

    def update_price(self, item, new_price):
        """Обновляет цену товара."""
        if item['price'] is None or new_price != item['price']:
            item['price'] = new_price
            item['date'] = datetime.now().strftime('%Y-%m-%d')
            item['status'] = 'found'
            self.log(f"Цена для товара '{item['name']}' обновлена: {item['price']}")
            message = {
                'product_id': item['id'],
                'product_name': item['name'],
                'message': f'Цена обновлена на {item["price"]}.',
                'timestamp': datetime.now().isoformat()  # Добавляем временную метку
            }
            self.messages.append(message)  # Сохраняем сообщение в список
        else:
            self.log(f"Цена для товара '{item['name']}' не изменилась.")

    def close(self, reason):
        """Сохраняет данные в файл только один раз при завершении работы."""
        self.save_messages_to_json()  # Сохранение сообщений в JSON файл
        self.send_logistic_messages()  # Отправка всех сообщений на Django
        self.save_to_file()
        self.log(f"Завершение работы паука. Причина: {reason}. Сообщения: {self.messages}")  # Логируем сообщения при закрытии

    def send_logistic_messages(self):
        """Отправляет все сообщения на адрес /logistic."""
        if not self.messages:  # Проверяем, есть ли сообщения
            self.log("Нет сообщений для отправки на /logistic.")
            return

        for message in self.messages:
            try:
                response = requests.post(f'{base_url}logistic/', json=message)
                if response.status_code == 200:
                    self.log("Сообщение успешно отправлено на /logistic.")
                else:
                    self.log(f"Ошибка при отправке сообщения на /logistic: {response.status_code}")
            except Exception as e:
                self.log(f"Исключение при отправке сообщения на /logistic: {str(e)}")

    def save_messages_to_json(self):
        """Сохраняет все сообщения в JSON файл."""
        if not self.messages:
            self.log("Нет сообщений для сохранения.")
            return
        
        log_file_path = f'../data_base/{self.endpoint}_messages.json'
        
        # Создаем директорию, если она не существует
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

        with open(log_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.messages, f, ensure_ascii=False, indent=4)
            self.log(f"Сообщения успешно сохранены в {log_file_path}")

    def save_to_file(self):
        """Сохраняет данные о товарах и отправляет их на сервер."""
        self.log(f"Сохраняем {len(self.products)} товаров в файл.")

        response = requests.post(f'{base_url}{self.endpoint}/', json=self.products)

        if response.status_code == 200:
            self.log("Данные успешно обновлены в базе данных.")
            # Добавляем сообщение об успешном обновлении данных
            message = {
                'message': 'Данные успешно обновлены.',
                'timestamp': datetime.now().isoformat()
            }
            self.messages.append(message)  # Сохраняем сообщение в список
        else:
            self.log(f"Ошибка при обновлении данных: {response.status_code}")

        with open(f'../data_base/{self.endpoint}.json', 'w', encoding='utf-8') as f:
            json.dump(self.products, f, ensure_ascii=False, indent=4)
            self.log(f"Товары сохранены в файл ../data_base/{self.endpoint}.json")

class UpdateFilters(BaseUpdateSpider):
    """Класс для обновления фильтров."""

    name = 'update_filters'
    start_urls = [f'{base_url}export-filters/']

    def __init__(self, *args, **kwargs):
        super(UpdateFilters, self).__init__('update_filters', *args, **kwargs)


class UpdatePumps(BaseUpdateSpider):
    """Класс для обновления насосов."""

    name = 'update_pumps'
    start_urls = [f'{base_url}export-pumps/']

    def __init__(self, *args, **kwargs):
        super(UpdatePumps, self).__init__('update_pumps', *args, **kwargs)
