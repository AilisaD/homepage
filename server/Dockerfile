FROM python:latest
RUN mkdir /homepage
WORKDIR /homepage
COPY server .
RUN pip install gunicorn
RUN python3 -m pip install -r requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/homepage"
EXPOSE 8080
CMD [ "gunicorn", "-c", "gunicorn.conf", "homepage:app"]