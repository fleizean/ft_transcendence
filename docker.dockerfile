FROM postgres:13

# Veritabanı adını ve kullanıcı adını ayarla
ENV POSTGRES_DB=pong
ENV POSTGRES_USER=indianpong
ENV POSTGRES_PASSWORD=indianpong123
ENV POSTGRES_HOST_AUTH_METHOD=trust

# Docker imajı oluşturulduğunda çalıştırılacak SQL dosyalarını kopyala

# PostgreSQL'in varsayılan bağlantı noktası
EXPOSE 5432

RUN pg_createcluster 13 main --start
RUN service postgresql start
