pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')