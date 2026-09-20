FROM ghcr.io/datagutten/rclaptimes AS static
RUN python /app/manage.py collectstatic --noinput
#RUN collectstatic --noinput

FROM nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

COPY --from=static /app/static /home/app/static