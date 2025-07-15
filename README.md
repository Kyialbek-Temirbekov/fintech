### Клонируйте репозиторий
```bash
git clone git@github.com:Kyialbek-Temirbekov/fintech.git
```
```bash
git clone https://github.com/Kyialbek-Temirbekov/fintech.git
```
### Перейдите в каталог проекта
```bash
cd fintech
```
### Соберите Docker-образы
```bash
docker compose build
```
### Запустите сервисы в фоновом режиме
```bash
docker compose up -d
```
### Загрузите тестовые данные (фикстуры)
```bash
docker compose exec web python manage.py loaddata test_data.json
```
### Перейдите по ссылке http://127.0.0.1:8000/accounts
### При необходимости остановите и удалите все контейнеры и тома базы данных
```bash
docker compose down -v
```
