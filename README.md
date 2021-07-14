1. Настроить ssl
(настроить сертификаты)

2. Установить 

sudo cp  .nginx/warehousebot.conf /etc/nginx/sites-enabled/default
sudo cp  .uwsgi/gunicorn.socket /etc/systemd/system/gunicorn.socket
sudo cp  .uwsgi/tgadmin.service /etc/systemd/system/tgadmin.service
sudo cp  .uwsgi/warehousebot.uwsgi.service /etc/systemd/system/warehousebot.uwsgi.service

3. Запустить сервисы  на сервере
sudo systemctl daemon-reload
sudo systemctl enable tgadmin
sudo systemctl start tgadmin
sudo systemctl enable warehousebot
sudo systemctl start warehousebot
