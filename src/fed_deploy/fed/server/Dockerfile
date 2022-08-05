FROM tensorflow/tensorflow
COPY . /server
WORKDIR /server
RUN /usr/bin/python3 -m pip install --upgrade pip
RUN pip3 install flwr sklearn
CMD python server.py
