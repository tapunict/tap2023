FROM apache/spark-py
ENV PATH $SPARK_DIR/bin:$PATH
ENV SPARK_VERSION=3.4.0
ENV SPARK_NLP=4.4.3
ENV HADOOP_VERSION=hadoop3
ENV SPARK_DIR=/opt/spark
ENV PATH $SPARK_DIR/bin:$PATH

USER root
RUN pip install spark-nlp==4.4.3 numpy

ENTRYPOINT [ "/opt/spark/bin/spark-submit" ]
#CMD [ "pyspark" ]