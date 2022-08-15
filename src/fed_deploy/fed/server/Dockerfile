FROM tensorflow/tensorflow
COPY . /server
WORKDIR /server
RUN /usr/bin/python3 -m pip install --upgrade pip
RUN pip3 install flwr sklearn
RUN python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps fed_pack
ENV partition="WrongDefault"
ENV server_id="WrongDefault"
ENV filename="WrongDefault"
ENV data_dir="WrongDefault"
CMD python server.py
