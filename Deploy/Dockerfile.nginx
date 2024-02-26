FROM nginx

# Create a directory for the certificates
RUN mkdir /etc/nginx/ssl

# Generate a self-signed certificate
RUN openssl req -x509 -newkey rsa:4096 -keyout /etc/nginx/ssl/key.pem -out /etc/nginx/ssl/cert.pem -days 365 -nodes -subj '/CN=localhost'

# Copy the Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf