FROM ubuntu:20.04

# install all dependencies as well as openssl 1.0.2
RUN apt-get update &&\
    apt-get -y remove openssl &&\
    DEBIAN_FRONTEND="noninteractive" apt-get -y install build-essential zlib1g-dev python2 python3-pip dh-autoreconf  libexpat1-dev gettext libz-dev  &&\
    DEBIAN_FRONTEND="noninteractive" apt-get -q update && apt-get -qy install wget libcurl4-gnutls-dev install-info make &&\
    wget https://www.openssl.org/source/openssl-1.0.2.tar.gz &&\
    tar -xzvf openssl-1.0.2.tar.gz &&\
    cd openssl-1.0.2 &&\
    ./config --prefix=/usr/local/ssl --openssldir=/usr/local/ssl shared zlib &&\
    make &&\
    make install

# install git including git-author and add it to the path
WORKDIR /git
RUN wget https://api.github.com/repos/mxz297/Git-author/tarball/master &&\
    tar -xzvf master &&\
    cd  mxz297-Git-author-2c4e5a0/git/ &&\
    make configure &&\
    ./configure --prefix=/usr &&\
    make install
ENV PATH /git/mxz297-Git-author-2c4e5a0/git:$PATH

# copy the source code
WORKDIR /src

# install tree-sitter
RUN pip install tree-sitter
RUN git clone https://github.com/tree-sitter/tree-sitter-c.git

# insert the target GitHub repository here
RUN git clone https://github.com/openssl/openssl.git
WORKDIR /src/openssl
RUN git checkout tags/openssl-3.2.0 -b openssl-3.2.0 
WORKDIR /src

COPY . .