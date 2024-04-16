FROM nginx:latest

# Nginx yapılandırma dosyasını değiştir
COPY nginx.conf /etc/nginx/nginx.conf

# SSL sertifikası ve anahtar dosyalarını kopyala
COPY ./localhost.crt /etc/nginx/certs/localhost.crt
COPY ./localhost.key /etc/nginx/certs/localhost.key