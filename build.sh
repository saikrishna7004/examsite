pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# echo "from django.contrib.auth.models import User; User.objects.create_superuser(username=191030001, password='admin', email='admin@email.com')" | python manage.py shell