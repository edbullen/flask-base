export FLASK_APP=base.py
echo "FLASK_APP name set to $FLASK_APP"

export POSTGRES_HOST="localhost"
export POSTGRES_PORT="5432"
export POSTGRES_DB="base"
export POSTGRES_USER="manager"

export LOG_NAME="webapp.log"
export LOG_DIR="./logs"
echo " "
echo "LOG_DIR set to $LOG_DIR"
echo "Manually export LOG_DIR to override"
echo " "

export POSTS_PER_PAGE="10"
echo "POSTS_PER_PAGE set to $POSTS_PER_PAGE"
echo " "

export MAIL_SERVER=smtp.googlemail.com
export MAIL_PORT=587
export MAIL_USE_TLS=1
#export MAIL_USERNAME=	
#export MAIL_PASSWORD=
echo "Please manually export MAIL_USERNAME"
echo "Please manually export MAIL_PASSWORD"
echo "Please manually export POSTGRES_PASSWORD"

