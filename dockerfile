FROM php:8.0-apache

# Install ekstensi PHP yang diperlukan
RUN docker-php-ext-install mysqli pdo_mysql
RUN a2enmod rewrite

# Restart Apache
RUN service apache2 restart

WORKDIR /var/www/html

COPY ./ ./
RUN rm -rf .git/*
RUN rm -rf .github/*

RUN chown www-data:www-data /var/www/html -R

EXPOSE 80