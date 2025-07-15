git clone ...
docker compose build
docker compose up -d
docker compose exec web python manage.py load data test_data.json
docker compose down -v
