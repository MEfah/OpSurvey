FROM nginx:1.25.4
COPY nginx/build/nginx.conf /etc/nginx/
COPY frontend/build /var/www/


