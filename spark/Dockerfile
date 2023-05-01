FROM amazoncorretto:17
ENV PATH $SPARK_DIR/bin:$PATH
ENV SPARK_VERSION=3.4.0
ENV HADOOP_VERSION=hadoop3
ENV SPARK_DIR=/opt/spark
ENV PATH $SPARK_DIR/bin:$PATH

ADD setup/spark-${SPARK_VERSION}-bin-${HADOOP_VERSION}.tgz /opt

RUN yum -y update && yum install -y procps gcc openssl-devel bzip2-devel libffi-devel wget tar make

#RUN wget https://www.python.org/ftp/python/3.11.1/Python-3.11.1.tgz && tar xzf Python-3.11.1.tgz && cd Python-3.11.1 && ./configure --enable-optimizations && make install   
RUN yum -y install python3

# RUN apt-get update && apt-get -y install bash python3 python3-pip netcat

RUN pip3 install pyspark numpy elasticsearch
# Create Sym Link 
RUN ln -s /opt/spark-${SPARK_VERSION}-bin-${HADOOP_VERSION} ${SPARK_DIR} 

ADD dataset /opt/tap/spark/dataset
# Add Python Code
ADD code/*  /opt/tap/
# Add Java Code
# ADD apps /opt/tap/apps
# Add Spark Manager
ADD spark-manager.sh $SPARK_DIR/bin/spark-manager

WORKDIR ${SPARK_DIR}
ENTRYPOINT [ "spark-manager" ]