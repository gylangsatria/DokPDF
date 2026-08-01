# Dockerfile
FROM nginx:alpine

# Copy application files
COPY index.html /usr/share/nginx/html/
COPY static/ /usr/share/nginx/html/static/
COPY favicon.ico /usr/share/nginx/html/

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create custom 404 page
RUN echo "<h1>404 - Halaman Tidak Ditemukan</h1><p>Kembali ke <a href='/'>DokPDF</a></p>" > /usr/share/nginx/html/404.html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]