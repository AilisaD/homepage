FROM python:latest
WORKDIR server
COPY . .
RUN pip install gunicorn
RUN pip install -r requirements.txt
CMD ["gunicorn", "server:app", "--bind", "0.0.0.0:7878", "--worker-class", "aiohttp.worker.GunicornWebWorker"]