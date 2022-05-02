FROM python:3.9
COPY . /
WORKDIR /
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN TIMEOUT=180
RUN KEEP_ALIVE=180
EXPOSE 7000
ENTRYPOINT [ "python" ]
CMD [ "deployment/main.py", "--reload"]