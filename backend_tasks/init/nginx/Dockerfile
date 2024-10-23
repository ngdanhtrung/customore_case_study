FROM nginx:1.21.1-alpine 
RUN apk add logrotate
# COPY ./dist /usr/share/nginx/html
# COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY ./nginx-logrotate.conf /etc/logrotate.d/nginx
RUN echo '*/5  *  *  *  * logrotate -fv /etc/logrotate.d/nginx' > /etc/crontabs/root
# RUN crond start
WORKDIR /usr/share/nginx/html
ENTRYPOINT ["nginx", "-g", "daemon off;"]