flowchart LR
    A[Crypto Price Producer] -->|JSON Messages| B[Kafka Topic: crypto_prices]
    B --> C[Spark Structured Streaming]
    C -->|Parse JSON + Transform| D[DataFrame]
    D -->|foreachBatch JDBC Write| E[MySQL Database]
    E --> F[crypto_prices Table]