echo "Building the project..."
pip install -r requirements.txt
pip install -U python-dotenv

echo "Make Migration..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "Collect Static..."
python3 manage.py collectstatic --noinput --clear
