# test_task_stripe_api

Данный проект можно посмотреть в "боевом" режиме по адресу: https://den90.pythonanywhere.com/


Запуск проекта локально:
  - Создаем директорию под проект, создаем виртуальное окружение и активируем его
  - Клонируем проект командой "git clone https://github.com/Den4ik-Bro/test_task_stripe_api.git"
  - Устанавливаем зависимости командой pip install -r requirements.txt
  - Создать .env файл и прописать в нем следующие переменные SECRET_KEY, DEBUG, STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY (последние две нужно получить 
  после регистрации на https://stripe.com по адресу https://dashboard.stripe.com/test/developers )
  - Выполняем миграции командой "python manage.py migrate" из директории проекта. При этом будут созданы три объекта "Item"
  - Создаем супер-пользователя командой python manage.py createsuperuser
  - Запускаем проект командой python manage.py runserver
  
Запуск с помощью докера:
  - Создаем директорию под проект, создаем виртуальное окружение и активируем его
  - Клонируем проект командой "git clone https://github.com/Den4ik-Bro/test_task_stripe_api.git"
  - Выполнить команды "docker-compose build" > "docker_compose up" и проект будет доступен по адресу 127.0.0.1:80000/
  
При создании объекта "Item" через админ панель или shell нужно указать stripe_product_id и stripe_price_id, 
для этого нужно зарегестрироваться на сайте https://stripe.com/ и создать товары в личном кабинете.

