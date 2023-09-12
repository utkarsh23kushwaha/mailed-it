echo "Building the project..."
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
pip install -U python-dotenv
python3 -m pip install pandas

echo "Make Migration..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "Collect Static..."
python3 manage.py collectstatic --noinput --clear
