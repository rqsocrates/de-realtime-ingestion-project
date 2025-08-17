#!/bin/bash

ENV_FILE=".env"

if grep -q "KAFKA_CLUSTER_ID" "$ENV_FILE"; then
    echo "KAFKA_CLUSTER_ID already set in $ENV_FILE:"
    grep "KAFKA_CLUSTER_ID" "$ENV_FILE"
else
    echo "Generating new KAFKA_CLUSTER_ID..."
    CLUSTER_ID=$(docker run --rm confluentinc/cp-kafka:7.5.0 kafka-storage random-uuid)
    echo "KAFKA_CLUSTER_ID=${CLUSTER_ID}" >> "$ENV_FILE"
    echo "KAFKA_CLUSTER_ID set to $CLUSTER_ID"
fi

