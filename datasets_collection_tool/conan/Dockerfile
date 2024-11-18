FROM ubuntu:20.04

# install all dependencies as well as openssl 1.0.2
RUN apt-get update &&\
    apt-get -y remove openssl &&\
    DEBIAN_FRONTEND="noninteractive" apt-get -y install build-essential zlib1g-dev python2 python3-pip dh-autoreconf  libexpat1-dev gettext libz-dev vim openjdk-17-jdk cmake unzip &&\
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

#setup Java for Ghidra
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64/
RUN export JAVA_HOME

#install Ghidra
ADD https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_11.0.3_build/ghidra_11.0.3_PUBLIC_20240410.zip /src/ghidra.zip
RUN unzip /src/ghidra.zip
RUN rm /src/ghidra.zip
RUN mkdir /src/ghidra_projects
RUN mkdir -p /src/analysis/analyzed_files

# install tree-sitter
RUN pip install tree-sitter
RUN git clone https://github.com/tree-sitter/tree-sitter-c.git
RUN git clone https://github.com/tree-sitter/tree-sitter-cpp.git

# install conan
RUN pip install conan
RUN git clone https://github.com/conan-io/conan-center-index.git

WORKDIR /src
RUN pip install pyyaml

COPY conan_profile /root/.conan2/profiles/default
COPY extract_various_formats.py /src/ghidra_11.0.3_PUBLIC/Ghidra/Features/Python/ghidra_scripts/extract_various_formats.py
COPY scripts/* .
