FROM python:3.7

MAINTAINER Gao JiaXiang "gaojxcs@gmail.com"

# RUN apt-get update && apt-get install -y \

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /pubmed_parser/requirements.txt

WORKDIR /pubmed_parser

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY . /pubmed_parser

ENTRYPOINT [ "python3" ]

CMD [ "-m", "server.flask_server" ]

