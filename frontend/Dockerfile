FROM nginx:alpine

# Upgrade Alpine OS packages to available patched versions
RUN apk upgrade --no-cache

COPY . /usr/share/nginx/html

EXPOSE 80
