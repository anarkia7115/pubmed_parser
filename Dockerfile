FROM centos

MAINTAINER Gao JiaXiang "gaojxcs@gmail.com"

RUN yum update -y && \
    yum install -y python-pip python-devel

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /pubmed_parser/requirements.txt

WORKDIR /pumed_parser

RUN pip install -r requirements.txt

COPY . /pumed_parser

ENTRYPOINT [ "python" ]

CMD [ "server/flask_server" ]

