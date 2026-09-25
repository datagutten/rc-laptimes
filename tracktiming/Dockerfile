FROM python:3.14 AS builder
RUN git clone https://github.com/CyberChacal/TrackTiming.git

FROM python:3.14-slim
RUN pip install flask pyzmq gunicorn
WORKDIR /app
COPY --from=builder /TrackTiming/files .
ENV TRACKTIMING_DATA="/data"
CMD gunicorn track_timing:app \
    --bind 0.0.0.0:80 \
    --workers 1 \
    --threads 4 \
    --timeout 30 \
    --access-logfile - \
    --error-logfile -