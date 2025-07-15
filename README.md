git clone git@github.com:Kyialbek-Temirbekov/fintech.git
git clone https://github.com/Kyialbek-Temirbekov/fintech.git
cd fintech
docker compose build
docker compose up -d
docker compose exec web python manage.py loaddata test_data.json
docker compose down -v
