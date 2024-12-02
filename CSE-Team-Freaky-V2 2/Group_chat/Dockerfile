FROM python:3

ENV HOME /root
WORKDIR /root

COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 8080

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait
#Missing the call to run the server itself.
CMD python3 manage.py runserver 0.0.0.0:8080
