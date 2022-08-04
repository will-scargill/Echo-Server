FROM python:3
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt \
  && mkdir -p /usr/src/app/data
VOLUME /usr/src/app/data
EXPOSE 16000
CMD ["server.py"]
ENTRYPOINT ["python3"]
