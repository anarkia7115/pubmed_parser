FROM centos

MAINTAINER Gao JiaXiang "gaojxcs@gmail.com"

RUN yum update -y && yum clean all

RUN yum -y install epel-release && yum clean all
RUN yum -y install python3-pip python3-devel && yum clean all
RUN yum -y install python3 gcc && yum clean all


# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /pubmed_parser/requirements.txt

WORKDIR /pubmed_parser

RUN pip install -r requirements.txt

COPY . /pubmed_parser

ENTRYPOINT [ "python3" ]

CMD [ "-m", "server.flask_server" ]

