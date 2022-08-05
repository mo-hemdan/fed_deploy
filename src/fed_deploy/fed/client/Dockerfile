FROM tensorflow/tensorflow
COPY . /client
WORKDIR /client
RUN python3 -m pip install --upgrade pip
RUN pip install flwr sklearn
ENV data_partition="WrongDefault"
ENV client_ip="WrongDefault"
ENV filename="WrongDefault"
CMD python client.py --partition=${data_partition} --client_id=${client_ip} --filename=${filename}