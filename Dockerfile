FROM python:slim
COPY . /src
WORKDIR /src
RUN pip3 install --upgrade pip && pip3 install -U -r requirements.txt
CMD bash -c 'python3 instagram/manage.py migrate && python3 instagram/manage.py runserver 0.0.0.0:8000'