FROM python:3.8
COPY . /monitor
WORKDIR /monitor
RUN python3 -m pip install --upgrade pip
RUN pip install flask
CMD python monitor.py