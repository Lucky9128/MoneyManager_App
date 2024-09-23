FROM python:3.9
RUN apt update -y 
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./ /code/

ARG FAST_API_HOST="127.0.0.1"
ARG FAST_API_PORT="9128"
ARG DB_HOST="mm_db_tb_cont"
ARG DB_PORT="5432"
ARG DB_PASS="pass"
ARG DB_DB="postgres"
ARG DB_USER="postgres"
ARG FAST_API_CONT="mm_api_cont"
ARG FAST_API_IMG="mm_api_img"
ARG DB_IMG="mm_db_tb_img"
ARG NET_NAME="my_net"


ENV FAST_API_HOST=${FAST_API_HOST}
ENV FAST_API_PORT=${FAST_API_PORT}
ENV DB_HOST=${DB_HOST}
ENV DB_PORT=${DB_PORT}
ENV DB_PASS=${DB_PASS}
ENV DB_DB=${DB_DB}
ENV DB_USER=${DB_USER}
ENV FAST_API_CONT=${FAST_API_CONT}
ENV FAST_API_IMG=${FAST_API_IMG}
ENV DB_IMG=${DB_IMG}
ENV NET_NAME=${NET_NAME}

CMD ["python3","app.py"]
