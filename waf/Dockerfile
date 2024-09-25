
FROM nginx/nginx-ingress:3.6.2

EXPOSE 80

EXPOSE 443

USER root

RUN apt-get update && apt-get install -y git build-essential libtool autoconf automake \
    pkg-config libpcre3-dev libxml2 libxml2-dev libyajl-dev libssl-dev

RUN git clone --recursive https://github.com/owasp-modsecurity/ModSecurity ModSecurity 

RUN cd ModSecurity && ./build.sh && ./configure && make && make install

USER nginx

