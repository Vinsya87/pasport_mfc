Простой проект под пару задач. Пользователь запрашивает услуги выдачи паспорта или замены. После каждого запроса ожидает ответа оператора(в обработке), либо отказано с указанием причины, либо выполнено и выдано. Если последние два, то можно снова запросить услугу.
и есть пользователь Оператор, который имеет возможность выполнять или отказывать услуги

python3.9 -m venv venv
. venv/bin/activate или source venv/bin/activate
pip3 install --upgrade pip
pip3 install -r requirements.txt
cd multi_center && python3 manage.py runserver
python3 manage.py makemigrations && python3 manage.py migrate
python3 manage.py createsuperuser
