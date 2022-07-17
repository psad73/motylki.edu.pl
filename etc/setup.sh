#!/bin/bash
# Przygotowanie systemu do instalacji aplikacji

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y python python-dev python-pip python-virtualenv supervisor
sudo apt-get install -y nginx git apache2-utils unzip
sudo apt-get install -y libxml2-dev libxslt1-dev build-essential


# ======================================
# PostgreSQL
# ======================================

sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib libpq-dev
# sudo -i -u postgres
sudo -u postgres createuser motylki_www  --no-createdb --no-superuser --no-createrole
sudo -u postgres createdb -O motylki_www motylki_www
sudo -u postgres psql -c "ALTER USER motylki_www WITH PASSWORD '@>S~?fHpC2?j/KasadefasdfvWe)lb@hujkl;t-f3'"


# ======================================
# Repo push2deploy
# ======================================

cd /opt/
git init --bare motylki.edu.pl.git

touch /opt/motylki.edu.pl.git/hooks/post-receive
chmod +x /opt/motylki.edu.pl.git/hooks/post-receive

cat > /opt/motylki.edu.pl.git/hooks/post-receive <<EOL
#!/bin/sh
GIT_WORK_TREE=/var/www/motylki.edu.pl git checkout -f master
supervisorctl restart motylki.edu.pl
EOL


# ======================================
# Aplikacja WWW
# ======================================

mkdir -p /var/www/motylki.edu.pl
cd /var/www/motylki.edu.pl

mkdir /var/www/motylki.edu.pl/logs
sudo chown -R :www-data /var/www/motylki.edu.pl/logs
sudo chmod -R g+rw /var/www/motylki.edu.pl/logs

mkdir /var/www/motylki.edu.pl/var
sudo chown -R :www-data /var/www/motylki.edu.pl/var
sudo chmod -R g+rw /var/www/motylki.edu.pl/var

mkdir /var/www/motylki.edu.pl/data
sudo chmod -R g+rw /var/www/motylki.edu.pl/data
sudo chown -R :www-data /var/www/motylki.edu.pl/data

mkdir /var/www/motylki.edu.pl/media
sudo chmod -R g+rw /var/www/motylki.edu.pl/media
sudo chown -R :www-data /var/www/motylki.edu.pl/media

# ======================================
# Vagrant development setup
# ======================================

sudo pip install virtualenvwrapper

echo "export WORKON_HOME=/home/vagrant/.virtualenvs" >> /home/vagrant/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> /home/vagrant/.bashrc
export WORKON_HOME=/home/vagrant/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

mkvirtualenv dev
/home/vagrant/.virtualenvs/dev/bin/pip install -r /vagrant/requirements.txt
/home/vagrant/.virtualenvs/vde/bin/pip install -r /vagrant/requirements-dev.txt

cp /vagrant/requirements.txt /var/www/motylki.edu.pl/

# ======================================
# Virtual environment
# ======================================

virtualenv /var/www/motylki.edu.pl/.pve

/var/www/motylki.edu.pl/.pve/bin/pip install -r /var/www/motylki.edu.pl/requirements.txt
/var/www/motylki.edu.pl/.pve/bin/pip install psycopg2

# /var/www/motylki.edu.pl/.pve/bin/python src/manage.py syncdb
# /var/www/motylki.edu.pl/.pve/bin/python src/manage.py migrate
# /var/www/motylki.edu.pl/.pve/bin/python src/manage.py loaddata fixtures/auth.json


# ======================================
# Nginx & Supervisor
# ======================================

ln -s /var/www/motylki.edu.pl/etc/supervisor.conf /etc/supervisor/conf.d/motylki.edu.pl.conf
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status

ln -s /var/www/motylki.edu.pl/etc/nginx.conf /etc/nginx/sites-available/motylki.edu.pl.conf
ln -s /etc/nginx/sites-available/motylki.edu.pl.conf /etc/nginx/sites-enabled/motylki.edu.pl.conf
rm /etc/nginx/sites-enabled/default
nginx -s reload
