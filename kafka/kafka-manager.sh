#!/bin/bash
ZK_DATA_DIR=/tmp/zookeeper
ZK_SERVER="localhost"

[[ -z "${KAFKA_ACTION}" ]] && { echo "KAFKA_ACTION required"; exit 1; }
[[ -z "${KAFKA_DIR}" ]] && { echo "KAFKA_DIR missing"; exit 1; }
[[ -z "${KAFKA_CONFIG}" ]] && { KAFKA_CONFIG="server.properties"; }
# ACTIONS start-zk, start-kafka, create-topic, 

echo "Running action ${KAFKA_ACTION} (Kakfa Dir:${KAFKA_DIR}, ZK Server: ${ZK_SERVER} Kafka Config ${KAFKA_CONFIG})"
 
case ${KAFKA_ACTION} in
    "start-zk")
    echo "Starting ZK"
    mkdir -p ${ZK_DATA_DIR}; # Data dir is setup in conf/zookeeper.properties
    zookeeper-server-start.sh ${KAFKA_DIR}/config/zookeeper.properties
    ;;
    "start-kafka")
    kafka-server-start.sh ${KAFKA_DIR}/config/${KAFKA_CONFIG}
    ;;
    "create-topic")
    kafka-topics.sh --create --bootstrap-server 10.0.100.23:9092 --replication-factor 1 --partitions 1 --topic ${KAFKA_TOPIC}
    ;;
    "producer")
    kafka-console-producer.sh --broker-list 10.0.100.23:9092 --topic ${KAFKA_TOPIC}
    ;;
    "consumer")
    kafka-console-consumer.sh --bootstrap-server 10.0.100.23:9092 --topic ${KAFKA_TOPIC} --from-beginning ${KAFKA_CONSUMER_PROPERTIES}
    ;;
    "connect-standalone")
    cd ${KAFKA_DIR}
    #connect-standalone-twitter.properties mysqlSinkTwitter.conf
    touch /tmp/my-test.txt
    connect-standalone.sh ${KAFKA_DIR}/config/${KAFKA_WORKER_PROPERTIES} ${KAFKA_CONNECTOR_PROPERTIES}
    #${KAFKA_DIR}/config/${KAFKA_CONNECTOR_PROPERTIES}  
    ;;
    "run-class")
    cd ${KAFKA_DIR}
    kafka-run-class.sh ${KAFKA_DIR}/${KAFKA_CLASS} --bootstrap-server 10.0.100.23:9092 --zookeeper 10.0.100.22:2181 --broker-list 10.0.100.23:9092 
    ;;
esac

echo "Done"