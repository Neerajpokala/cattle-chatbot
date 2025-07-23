# 🐄 Cattle Insights Chatbot - Complete Documentation

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [Database Schema](#database-schema)
- [API Reference](#api-reference)
- [Query Examples](#query-examples)
- [Troubleshooting](#troubleshooting)
- [Deployment](#deployment)
- [Contributing](#contributing)

## 🔍 Overview

The Cattle Insights Chatbot is an intelligent conversational interface for monitoring and querying cattle behavior data. Built with Streamlit and powered by machine learning inference data, it provides real-time insights into cattle health, behavior, location, and accelerometer readings through natural language queries.

### Key Capabilities
- **Natural Language Processing**: Understands queries in plain English
- **Real-time Data Access**: Queries live inference data from cattle sensors
- **Multi-metric Support**: Temperature, behavior, location, accelerometer data, and health status
- **Interactive Interface**: Web-based chat interface with debug capabilities
- **Production Ready**: Comprehensive logging, error handling, and performance optimization

## ✨ Features

### 🤖 Core Functionality
- **Natural Language Understanding**: Processes queries like "What is the temperature of cow-101?"
- **Entity Extraction**: Automatically identifies cow IDs, metrics, and time contexts
- **SQL Generation**: Converts natural language to optimized database queries
- **Response Generation**: Formats database results into human-readable responses
- **Real-time Processing**: Instant query processing with loading indicators

### 📊 Supported Queries
- **Temperature Monitoring**: Current and historical temperature data
- **Behavior Analysis**: Current activities (grazing, walking, resting, etc.)
- **Health Assessment**: Automated health status evaluation
- **Location Tracking**: GPS coordinates and position data
- **Accelerometer Data**: Raw sensor readings (AccX, AccY, AccZ)
- **Activity Levels**: Movement intensity measurements

### 🎯 User Interface Features
- **Interactive Chat**: Streamlit-based conversational interface
- **Quick Actions**: Pre-defined buttons for common queries
- **Debug Sidebar**: Real-time query analysis and SQL generation
- **Data Visualization**: Retrieved data display for transparency
- **Session Management**: Persistent chat history during session

## 🏗️ System Architecture

### Component Overview

```
User Query → NLP Processing → SQL Generation → Database Query → Response Formatting
     ↓              ↓               ↓               ↓               ↓
"What is the    Extract Intent   Generate SQL    Execute on      Format Natural
temperature     & Entities       Query           SQLite DB       Language Response
of cow-101?"    (cow-101,        SELECT temp     cattle_inference "Bessie's temp
                temperature)     WHERE...        table           is 38.5°C"
```

### Architecture Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   Query         │    │   SQL           │
│   Interface     │───▶│   Processor     │───▶│   Generator     │
│   (app.py)      │    │   (NLP)         │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
┌─────────────────┐    ┌─────────────────┐           ▼
│   Response      │    │   Database      │    ┌─────────────────┐
│   Generator     │◀───│   Connection    │◀───│   SQLite        │
│                 │    │   (SQLAlchemy)  │    │   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Streamlit | Interactive web interface |
| **Backend** | Python 3.12+ | Core application logic |
| **Database** | SQLite + SQLAlchemy | Data storage and queries |
| **NLP** | Regex + spaCy | Natural language processing |
| **Deployment** | Streamlit Cloud | Web hosting and deployment |

## 🚀 Installation & Setup

### Prerequisites

- **Python 3.7+**
- **Git** (for cloning repository)
- **500MB** free disk space
- **Internet connection** (for package installation)

### Step 1: Clone Repository

```bash
git clone https://github.com/your-username/cattle-chatbot.git
cd cattle-chatbot
```

### Step 2: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm
```

### Step 3: Create Database

```bash
# Navigate to database directory
cd database

# Create SQLite database with sample data
python models.py

# Return to main directory
cd ..
```

### Step 4: Run Application

```bash
# Launch Streamlit application
streamlit run app.py
```

### Project Structure

```
cattle-chatbot/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── config.py                # Configuration settings
├── view.py                  # Data export utility
├── .env                     # Environment variables (optional)
├── database/
│   ├── __init__.py
│   ├── models.py            # Database schema and sample data
│   ├── connection.py        # Database connection management
│   └── cattle_monitoring.db # SQLite database file
├── chatbot/
│   ├── __init__.py
│   ├── query_processor.py   # Natural language processing
│   ├── sql_generator.py     # SQL query generation
│   ├── response_generator.py # Response formatting
│   └── main_controller.py   # Main chatbot orchestration
└── tests/
    └── test_chatbot.py      # Unit tests (optional)
```

## 📖 Usage Guide

### Basic Usage

1. **Start the Application**
   ```bash
   streamlit run app.py
   ```

2. **Access the Interface**
   - Open your browser to `http://localhost:8501`
   - The chatbot interface will load automatically

3. **Ask Questions**
   - Type questions in the chat input at the bottom
   - Use natural language like "What is the temperature of cow-101?"
   - Click "Send" or press Enter

### Sample Queries

#### Temperature Queries
```
- "What is the temperature of cow-101?"
- "Show me cow-102's current temperature"
- "What is Bessie's temp?"
```

#### Behavior Queries
```
- "What is cow-103 doing?"
- "Show me cow-104's behavior"
- "What activity is Moobert performing?"
```

#### Health Queries
```
- "Is cow-105 healthy?"
- "Check cow-101's health status"
- "Any health alerts for Daisy?"
```

#### Location Queries
```
- "Where is cow-102?"
- "Show me cow-103's location"
- "What are Bessie's coordinates?"
```

#### Accelerometer Queries
```
- "Show me cow-101's accelerometer data"
- "What is cow-102's AccX value?"
- "Display movement data for cow-103"
```

### Interface Components

#### Main Chat Area
- **Message History**: Shows conversation between user and bot
- **Chat Input**: Text field for entering questions
- **Send Button**: Submits query to chatbot

#### Sidebar Features
- **Available Cows**: List of cattle in the database
- **Query Analysis**: Real-time breakdown of query processing
- **Generated SQL**: Shows the actual database query executed
- **Retrieved Data**: Raw data returned from database

#### Quick Actions
- **🌡️ Check Temperature**: Sample temperature query
- **🏥 Health Check**: Sample health assessment
- **📊 Accelerometer Data**: Sample sensor data query
- **🗑️ Clear Chat**: Reset conversation history

## 🗄️ Database Schema

### Tables Overview

The chatbot uses two main tables to store cattle information and inference data:

#### `cattle_devices` Table

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `device_id` | String(50) | Primary key, unique device identifier | cow-101 |
| `cow_id` | String(50) | Internal cow identification | COW001 |
| `cow_name` | String(100) | Human-readable cow name | Bessie |

#### `cattle_inference` Table

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `id` | Integer | Auto-increment primary key | 1 |
| `device_id` | String(50) | Links to cattle_devices | cow-101 |
| `timestamp` | DateTime | When reading was taken | 2024-12-15 14:30:22 |
| `predicted_behavior` | String(50) | ML model prediction | grazing |
| `confidence` | Float | Model confidence (0.0-1.0) | 0.92 |
| `temperature` | Float | Body temperature (°C) | 38.5 |
| `location_lat` | Float | GPS latitude | 40.712776 |
| `location_lng` | Float | GPS longitude | -74.005974 |
| `activity_level` | Float | Movement intensity (0.0-1.0) | 0.7 |
| `AccX` | Float | X-axis acceleration (g-force) | 0.234 |
| `AccY` | Float | Y-axis acceleration (g-force) | 1.567 |
| `AccZ` | Float | Z-axis acceleration (g-force) | 0.890 |
| `created_at` | DateTime | Record creation timestamp | 2024-12-15 14:30:22 |

### Sample Data

The database comes pre-populated with realistic sample data:

- **5 Cattle Devices**: cow-101 through cow-105
- **125 Inference Records**: 25 historical readings per cow
- **Cow Names**: Bessie, Daisy, Moobert, Luna, Ruby
- **Realistic Values**: Temperature (38-40°C), varied behaviors, GPS coordinates

### Database Relationships

```sql
cattle_devices.device_id ←→ cattle_inference.device_id (One-to-Many)
```

## 🔧 API Reference

### Core Classes

#### `CattleChatbot`

Main orchestrator class that coordinates all chatbot components.

```python
class CattleChatbot:
    def __init__(self)
    def chat(self, user_message: str) -> str
```

**Methods:**
- `chat(user_message)`: Process user query and return response

#### `SimpleQueryProcessor`

Handles natural language understanding and entity extraction.

```python
class SimpleQueryProcessor:
    def __init__(self)
    def extract_cow_id(self, query: str) -> str
    def extract_metric(self, query: str) -> str
    def extract_time_context(self, query: str) -> str
    def process_query(self, query: str) -> Dict
```

**Methods:**
- `extract_cow_id()`: Find cow ID in query (e.g., "cow-101")
- `extract_metric()`: Identify requested metric (temperature, behavior, etc.)
- `extract_time_context()`: Determine time frame (current, yesterday, etc.)
- `process_query()`: Complete query analysis

#### `SimpleSQLGenerator`

Converts processed queries into SQL statements.

```python
class SimpleSQLGenerator:
    def __init__(self)
    def generate_query(self, processed_query: Dict) -> str
```

**Methods:**
- `generate_query()`: Create SQL query from processed natural language

#### `SimpleResponseGenerator`

Formats database results into natural language responses.

```python
class SimpleResponseGenerator:
    def __init__(self)
    def generate_response(self, processed_query: Dict, results: pd.DataFrame, db_connection) -> str
    def _generate_health_response(self, data: Dict) -> str
```

**Methods:**
- `generate_response()`: Create human-readable response from data
- `_generate_health_response()`: Specialized health assessment logic

#### `DatabaseConnection`

Manages SQLite database connections and query execution.

```python
class DatabaseConnection:
    def __init__(self)
    def execute_query(self, query: str) -> pd.DataFrame
    def test_connection(self) -> bool
    def get_available_cows(self) -> pd.DataFrame
```

**Methods:**
- `execute_query()`: Run SQL query and return DataFrame
- `test_connection()`: Verify database connectivity
- `get_available_cows()`: Get list of available cattle

### Configuration

#### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | True | Enable debug mode |
| `PAGE_TITLE` | Cattle Insights Chatbot | Application title |
| `PAGE_ICON` | 🐄 | Browser tab icon |

#### Customizable Parameters

```python
# Query processing patterns
cow_pattern = r'cow[_-]?(\d+)'
metric_keywords = {
    'temperature': ['temperature', 'temp', 'fever'],
    'behavior': ['behavior', 'activity', 'doing'],
    # ... add more keywords
}

# Health thresholds
TEMP_HIGH_THRESHOLD = 39.5  # °C
TEMP_LOW_THRESHOLD = 38.0   # °C
```

## 💬 Query Examples

### Basic Queries

#### Single Cow Information
```
User: "What is the temperature of cow-101?"
Bot: "🌡️ Bessie currently has a temperature of 38.5°C"

User: "What is cow-102 doing?"
Bot: "🐄 Daisy is currently grazing (confidence: 92.0%)"

User: "Where is cow-103?"
Bot: "📍 Moobert is at coordinates (40.7128, -74.0060)"
```

#### Health Assessment
```
User: "Is cow-101 healthy?"
Bot: "✅ Bessie appears healthy (temp: 38.5°C)"

User: "Is cow-104 sick?"
Bot: "⚠️ Luna health alert: high temperature (40.2°C)"
```

#### Accelerometer Data
```
User: "Show me cow-105's accelerometer data"
Bot: "📊 Ruby accelerometer: X=0.234g, Y=1.567g, Z=0.890g"

User: "What is cow-101's AccX value?"
Bot: "📊 Bessie accelerometer: X=0.156g, Y=0.789g, Z=1.023g"
```

### Advanced Queries

#### Multiple Metrics
```
User: "Tell me about cow-102"
Bot: "📊 Daisy: walking, 38.8°C, Activity: 80.0%"
```

#### Time-based Queries
```
User: "What was cow-103's temperature yesterday?"
Bot: "🌡️ Moobert had a temperature of 39.1°C yesterday"
```

#### Partial Cow Names
```
User: "How is Bessie doing?"
Bot: "🐄 Bessie is currently grazing (confidence: 94.2%)"
```

### Health Assessment Logic

The chatbot uses the following rules for health evaluation:

#### Temperature Thresholds
- **Normal**: 38.0°C - 39.5°C
- **Low**: < 38.0°C (hypothermia concern)
- **High**: > 39.5°C (fever concern)

#### Health Status Responses
```python
if temperature > 39.5:
    return "⚠️ {cow_name} health alert: high temperature ({temp}°C)"
elif temperature < 38.0:
    return "⚠️ {cow_name} health alert: low temperature ({temp}°C)"
else:
    return "✅ {cow_name} appears healthy (temp: {temp}°C)"
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Database Connection Errors

**Problem**: `Database connection error: no such table: cattle_devices`

**Solution**:
```bash
cd database
python models.py
cd ..
streamlit run app.py
```

#### 2. Module Import Errors

**Problem**: `ImportError: cannot import name 'Config' from 'config'`

**Solution**: Create `config.py` file:
```python
class Config:
    PAGE_TITLE = "🐄 Cattle Insights Chatbot"
    PAGE_ICON = "🐄"
    DEBUG = True
```

#### 3. No Query Results

**Problem**: Chatbot returns "No data found for that cow"

**Causes & Solutions**:
- **Wrong cow ID**: Use cow-101, cow-102, etc. (not cow101)
- **Empty database**: Run `python database/models.py` to create sample data
- **Database corruption**: Delete `cattle_monitoring.db` and recreate

#### 4. Streamlit Port Already in Use

**Problem**: `Port 8501 is already in use`

**Solution**:
```bash
# Use different port
streamlit run app.py --server.port 8502

# Or kill existing process
lsof -ti:8501 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8501   # Windows
```

#### 5. Package Installation Issues

**Problem**: `pip install` failures

**Solution**:
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install with --user flag
pip install --user -r requirements.txt

# Use virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Debug Features

#### Sidebar Debug Information

The chatbot provides real-time debugging in the sidebar:

1. **Query Analysis**: Shows extracted entities
   ```json
   {
     "cow_id": "cow-101",
     "metric": "temperature",
     "time_context": "current"
   }
   ```

2. **Generated SQL**: Displays actual database query
   ```sql
   SELECT ci.device_id, cd.cow_name, ci.temperature
   FROM cattle_inference ci
   LEFT JOIN cattle_devices cd ON ci.device_id = cd.device_id
   WHERE ci.device_id = 'cow-101'
   ORDER BY ci.timestamp DESC LIMIT 1
   ```

3. **Retrieved Data**: Shows raw database results
   ```json
   {
     "device_id": "cow-101",
     "cow_name": "Bessie",
     "temperature": 38.5,
     "timestamp": "2024-12-15 14:30:22"
   }
   ```

#### Logging

Enable detailed logging by setting environment variables:
```bash
export DEBUG=True
export LOG_LEVEL=DEBUG
```

### Performance Optimization

#### Database Optimization
- **Indexes**: Automatic indexes on `device_id` and `timestamp`
- **Query Limits**: All queries limited to 10 results max
- **Connection Caching**: SQLAlchemy connections cached via Streamlit

#### Memory Management
- **Session State**: Only chat history stored in session
- **Data Cleanup**: No persistent data storage beyond database

## 🌐 Deployment

### Local Deployment

#### Development Mode
```bash
streamlit run app.py
```

#### Production Mode
```bash
streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false
```

### Cloud Deployment

#### Streamlit Cloud

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Deploy cattle chatbot"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `app.py` as main file
   - Deploy automatically

3. **Environment Variables**:
   ```
   DEBUG=False
   ```

#### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t cattle-chatbot .
docker run -p 8501:8501 cattle-chatbot
```

#### AWS/GCP/Azure

The application can be deployed on any cloud platform supporting Python web applications:

- **AWS**: Elastic Beanstalk, ECS, or Lambda
- **GCP**: App Engine or Cloud Run
- **Azure**: App Service or Container Instances

### Production Considerations

#### Security
- **Database**: Use proper authentication for production databases
- **HTTPS**: Enable SSL certificates for web traffic
- **Input Validation**: Additional sanitization for user inputs

#### Scalability
- **Database**: Consider PostgreSQL or MySQL for larger datasets
- **Caching**: Implement Redis for query result caching
- **Load Balancing**: Use multiple instances for high traffic

#### Monitoring
- **Logging**: Implement structured logging with log aggregation
- **Metrics**: Track query response times and error rates
- **Alerts**: Set up notifications for system issues

## 🤝 Contributing

### Development Setup

1. **Fork Repository**
   ```bash
   git clone https://github.com/your-username/cattle-chatbot.git
   cd cattle-chatbot
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Run Tests**
   ```bash
   python -m pytest tests/
   ```

### Code Style

- **Follow PEP 8** for Python code formatting
- **Use type hints** where appropriate
- **Add docstrings** to all functions and classes
- **Keep functions small** and focused on single responsibility

### Adding New Features

#### New Query Types

1. **Update Query Processor**:
   ```python
   # Add new metric to metric_keywords
   self.metric_keywords['new_metric'] = ['keyword1', 'keyword2']
   ```

2. **Update Response Generator**:
   ```python
   # Add new response template
   self.templates['new_metric'] = "📊 {cow_name} new metric: {value}"
   ```

3. **Update SQL Generator** (if needed):
   ```python
   # Add new columns to base query if required
   ```

#### New Database Fields

1. **Update Database Schema**:
   ```python
   # Add new column to cattle_inference table
   Column("new_field", Float),
   ```

2. **Create Migration Script**:
   ```python
   # Script to update existing databases
   ```

3. **Update Sample Data**:
   ```python
   # Include new field in sample data generation
   ```

### Testing

#### Unit Tests

Create tests in `tests/` directory:
```python
def test_cow_id_extraction():
    processor = SimpleQueryProcessor()
    result = processor.extract_cow_id("What is cow-101 doing?")
    assert result == "cow-101"
```

#### Integration Tests

Test complete query flow:
```python
def test_temperature_query():
    chatbot = CattleChatbot()
    response = chatbot.chat("What is the temperature of cow-101?")
    assert "temperature" in response.lower()
    assert "Bessie" in response
```

### Pull Request Process

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/new-feature-name
   ```

2. **Make Changes and Test**:
   ```bash
   python -m pytest tests/
   ```

3. **Commit Changes**:
   ```bash
   git add .
   git commit -m "Add new feature: description"
   ```

4. **Push and Create PR**:
   ```bash
   git push origin feature/new-feature-name
   ```

5. **Follow PR Template** and await review

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit Team**: For the excellent web application framework
- **SQLAlchemy**: For robust database ORM capabilities
- **spaCy**: For natural language processing tools
- **Pandas**: For efficient data manipulation
- **Open Source Community**: For inspiration and best practices

## 📞 Support

### Getting Help

- **GitHub Issues**: [Create an issue](https://github.com/your-username/cattle-chatbot/issues)
- **Documentation**: This comprehensive guide
- **Community**: Join discussions in GitHub Discussions

### FAQ

**Q: Can I use this with real cattle data?**
A: Yes! Replace the sample data with your actual inference results from your ML models.

**Q: How do I add more cattle?**
A: Insert new records into the `cattle_devices` table and corresponding inference data.

**Q: Can I deploy this commercially?**
A: Yes, the MIT license allows commercial use. Consider security and scalability requirements.

**Q: How do I backup my data?**
A: Use the `view.py` script to export all data to CSV files.

---

**🐄 Ready to monitor your cattle with intelligent conversations!**

This chatbot provides a natural, intuitive way to access cattle monitoring data through simple conversation. The modular architecture makes it easy to extend and customize for your specific needs.
