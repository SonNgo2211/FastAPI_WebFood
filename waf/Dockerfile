
FROM nginx/nginx-ingress:3.6.2

EXPOSE 80

EXPOSE 443

USER root

RUN apt-get update && apt-get install -y git build-essential libtool autoconf automake \
    pkg-config libpcre3-dev libxml2 libxml2-dev libyajl-dev libssl-dev

RUN git clone --recursive https://github.com/owasp-modsecurity/ModSecurity ModSecurity 

RUN cd ModSecurity && ./build.sh && ./configure && make && make install

RUN git clone --depth 1 https://github.com/owasp-modsecurity/ModSecurity-nginx.git

COPY auto /etc/nginx/auto

COPY configure /etc/nginx

WORKDIR /etc/nginx

RUN apt-get install -y apt-utils libcurl4-openssl-dev libgeoip-dev liblmdb-dev \
    pkgconf zlib1g-dev

RUN ./configure --with-compat --add-dynamic-module=/ModSecurity-nginx

COPY src /etc/nginx/src

RUN make modules

RUN cp objs/ngx_http_modsecurity_module.so /etc/nginx/modules/

COPY nginx.conf /etc/nginx/

RUN mkdir -p /etc/nginx/modsecurity/rules

RUN mkdir -p /etc/nginx/modsecurity/config

RUN chown -R nginx: /etc/nginx

WORKDIR /

USER nginx

