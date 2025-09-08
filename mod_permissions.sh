sudo su
touch package-lock.json
mkdir -p node_modules home
chown -R www-data:www-data celerybeat-schedule package-lock.json media node_modules home
chown -R www-data:www-data static
chown gtoscano:www-data static_files
chown gtoscano:www-data static_files/css
chmod 775 static_files static_files/css

