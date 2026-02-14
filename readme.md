## 🏗️ System Architecture

```mermaid
flowchart TD

    A[Crypto Price Producer<br/>Python Script] 
    B[Apache Kafka<br/>Topic: crypto_prices]
    C[Apache Spark<br/>Structured Streaming Engine]
    D[Data Parsing & Transformation<br/>JSON → Structured DataFrame]
    E[foreachBatch Processing<br/>Micro-batch Execution]
    F[(MySQL Database<br/>crypto_db)]
    G[(Table: crypto_prices)]

    A -->|Send JSON Messages| B
    B -->|Stream Consumption| C
    C --> D
    D --> E
    E -->|JDBC Write| F
    F --> G
```
