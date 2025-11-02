# AskMyPDF - AI-Powered PDF Resume Analyzer

A FastAPI-based application that allows users to upload PDF resumes and get AI-powered analysis using Google's Gemini AI. The application converts PDF pages to images and uses Gemini's vision capabilities to analyze and provide feedback on resumes.

## 🚀 Features

- **PDF Upload**: Upload PDF files through a REST API
- **Async Processing**: Background job processing using Redis Queue (RQ)
- **AI Analysis**: Powered by Google Gemini AI for intelligent resume analysis
- **MongoDB Storage**: Persistent storage for file metadata and analysis results
- **Status Tracking**: Real-time status updates throughout the processing pipeline
- **Docker Support**: Fully containerized development environment

## 📋 Table of Contents

- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [Development](#development)
- [Environment Variables](#environment-variables)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## 🏗️ Architecture

The application follows a microservices-inspired architecture:

1. **API Layer** (FastAPI): Handles HTTP requests and file uploads
2. **Queue System** (Redis + RQ): Manages background job processing
3. **Database Layer** (MongoDB): Stores file metadata and processing results
4. **AI Processing** (Gemini AI): Analyzes PDF content using vision models
5. **Storage Layer**: File system storage for uploaded PDFs and converted images

### Processing Flow

```
Upload PDF → Save to MongoDB → Queue Job → Convert to Images → AI Analysis → Update Results
```

## 📦 Prerequisites

- Docker and Docker Compose
- VS Code with Dev Containers extension (recommended)
- Google API Key for Gemini AI

## 🛠️ Installation

### Option 1: Using Dev Containers (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd AskMyPDF
```

2. Open in VS Code:
```bash
code .
```

3. When prompted, click "Reopen in Container" or use Command Palette:
   - Press `F1` or `Ctrl+Shift+P`
   - Select "Dev Containers: Reopen in Container"

4. Wait for the container to build and start

5. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Option 2: Local Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AskMyPDF
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install system dependencies:
```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# macOS
brew install poppler
```

5. Set up MongoDB and Redis (or use Docker):
```bash
docker-compose -f .devcontainer/docker-compose.yaml up mongo valkey -d
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Google Gemini AI
GOOGLE_API_KEY=your_google_api_key_here

# MongoDB Configuration
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_USER=admin
MONGO_PASS=admin
MONGO_URI=mongodb://admin:admin@localhost:27017

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
```

### Getting a Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

## 🚀 Usage

### Starting the Application

#### Using the run script:
```bash
chmod +x run.sh
./run.sh
```

#### Or manually:
```bash
uvicorn app.server:app --host 0.0.0.0 --port 8000 --reload
```

#### Starting the Worker:
In a separate terminal, start the RQ worker:
```bash
rq worker --with-scheduler
```

### API Access

The API will be available at: `http://localhost:8000`

API Documentation (Swagger UI): `http://localhost:8000/docs`

## 📡 API Endpoints

### Health Check
```http
GET /
```

**Response:**
```json
{
  "status": "healthy"
}
```

### Upload PDF
```http
POST /upload
Content-Type: multipart/form-data
```

**Parameters:**
- `file`: PDF file (multipart/form-data)

**Response:**
```json
{
  "file_id": "507f1f77bcf86cd799439011"
}
```

### Get File Status
```http
GET /{id}
```

**Parameters:**
- `id`: File ID returned from upload

**Response:**
```json
{
  "_id": "507f1f77bcf86cd799439011",
  "name": "resume.pdf",
  "status": "processed",
  "result": "AI analysis result here..."
}
```

**Status Values:**
- `saving`: File is being saved to disk
- `queued`: Job is queued for processing
- `processing`: Processing has started
- `converting to images`: PDF is being converted to images
- `converting to images success`: Conversion completed
- `analyzing with AI`: Gemini AI is analyzing the content
- `processed`: Analysis complete
- `failed`: Processing failed

## 📁 Project Structure

```
AskMyPDF/
├── .devcontainer/
│   ├── devcontainer.json      # VS Code dev container config
│   ├── docker-compose.yaml    # Docker services (MongoDB, Valkey)
│   └── Dockerfile             # Python development container
├── .vscode/
│   └── settings.json          # VS Code workspace settings
├── app/
│   ├── db/
│   │   ├── collections/
│   │   │   ├── __init__.py
│   │   │   └── file.py        # File collection schema
│   │   ├── __init__.py
│   │   ├── client.py          # MongoDB client setup
│   │   └── db.py              # Database initialization
│   ├── queue/
│   │   ├── __init__.py
│   │   ├── q.py               # Redis queue setup
│   │   └── workers.py         # Background job workers
│   ├── utils/
│   │   ├── __init__.py
│   │   └── file.py            # File handling utilities
│   ├── main.py                # Application entry point
│   └── server.py              # FastAPI application
├── .env                       # Environment variables (create this)
├── .gitignore                 # Git ignore rules
├── freeze.sh                  # Script to freeze dependencies
├── requirements.txt           # Python dependencies
├── run.sh                     # Development server script
└── README.md                  # This file
```

## 🔧 Development

### Freezing Dependencies

After installing new packages, update requirements.txt:
```bash
pip freeze > requirements.txt
```

Or use the provided script:
```bash
chmod +x freeze.sh
./freeze.sh
```

**Note**: The project uses a simplified requirements.txt with unpinned versions to avoid dependency conflicts. If you need to pin specific versions, test thoroughly with your Python version.

### Running Tests

```bash
pytest
```

### Code Formatting

The dev container is configured with:
- Black formatter (auto-format on save)
- Flake8 linting
- isort for import sorting

### Adding New Dependencies

```bash
pip install <package-name>
./freeze.sh  # Update requirements.txt
```

## 🌍 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google Gemini API key | Required |
| `MONGO_HOST` | MongoDB host | `localhost` |
| `MONGO_PORT` | MongoDB port | `27017` |
| `MONGO_USER` | MongoDB username | `admin` |
| `MONGO_PASS` | MongoDB password | `admin` |
| `MONGO_URI` | Full MongoDB connection string | Auto-generated |
| `REDIS_HOST` | Redis/Valkey host | `valkey` |
| `REDIS_PORT` | Redis/Valkey port | `6379` |

## 🛠️ Technologies Used

- **FastAPI**: Modern, fast web framework for building APIs
- **MongoDB**: NoSQL database for storing file metadata
- **Redis/Valkey**: In-memory data store for job queuing
- **RQ (Redis Queue)**: Simple Python library for queueing jobs
- **Google Gemini AI**: Advanced AI model for content analysis
- **pdf2image**: Convert PDF pages to images
- **Pillow**: Python Imaging Library
- **Uvicorn**: ASGI server for FastAPI
- **Pydantic**: Data validation using Python type annotations
- **aiofiles**: Async file operations

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat(scope): add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Commit Message Convention

Follow the conventional commits specification:
```
feat(scope): description
fix(scope): description
docs(scope): description
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini AI for providing the AI analysis capabilities
- FastAPI community for the excellent framework
- MongoDB and Redis communities

## 📞 Support

For issues, questions, or contributions, please open an issue on GitHub.

---

**Made with ❤️ for the ChaiCode GenAI Cohort**

