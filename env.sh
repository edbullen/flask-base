export FLASK_APP=base.py
echo "FLASK_APP is $FLASK_APP"

export POSTGRES_HOST="localhost"
export POSTGRES_PORT="5432"
export POSTGRES_DB="base"
export POSTGRES_USER="manager"

export MAIL_SERVER=smtp.googlemail.com
export MAIL_PORT=587
export MAIL_USE_TLS=1
#export MAIL_USERNAME=	
#export MAIL_PASSWORD=
echo "Please manually set MAIL_USERNAME"
echo "Please manually set MAIL_PASSWORD"
echo "Please manually set POSTGRES_PASSWORD"

