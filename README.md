# Stock Service

A microservice for managing stock transactions and portfolios.

## Features

- Transaction management
- Portfolio tracking
- Message processing with Apache Kafka
- Temporal workflows

## Prerequisites

- Python 3.8+
- PostgreSQL
- Apache Kafka
- Temporal

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/stock-service.git
cd stock-service
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
# Create a PostgreSQL database named 'stock_service'
createdb stock_service
```

5. Start Kafka:
```bash
# Start Zookeeper
zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties

# Start Kafka
kafka-server-start /usr/local/etc/kafka/server.properties
```

6. Start Temporal:
```bash
temporal server start-dev
```

## Running the Service

1. Start the API server:
```bash
uvicorn src.entrypoints.api:app --reload
```

2. Start the message consumer:
```bash
python -m src.entrypoints.consumer
```

3. Start the workflow worker:
```bash
python -m src.entrypoints.workflow
```

## API Documentation

Once the service is running, you can access:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## Project Structure

```
src/
├── domain/           # Domain models and interfaces
├── usecases/         # Application use cases
├── infrastructure/   # Implementation details
│   ├── config/      # Configuration
│   ├── messaging/   # Kafka messaging
│   ├── repositories/# Repository implementations
│   └── workflow/    # Temporal workflows
└── entrypoints/     # API and worker entrypoints
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
