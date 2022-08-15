FROM tensorflow/tensorflow
COPY . /client
WORKDIR /client
RUN python3 -m pip install --upgrade pip
RUN pip install flwr sklearn
RUN python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps fed_pack
ENV partition="WrongDefault"
ENV client_id="WrongDefault"
ENV filename="WrongDefault"
ENV data_dir="WrongDefault"
ENV server_ip="WrongDefault"
ENV monitor_ip="WrongDefault"
CMD python client.py