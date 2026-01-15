# 🔐 Password Security Analyzer

A modern, full-stack application that analyzes password strength and security in real-time. Built with FastAPI (Python) backend and Next.js (React) frontend, this tool helps users create stronger, more secure passwords by providing instant feedback on password quality, entropy, pattern detection, and breach status.

## 🌐 Live Deployment

- **Frontend**: [https://password-security-analyzer-mu.vercel.app/](https://password-security-analyzer-mu.vercel.app/)
- **Backend API**: [https://password-security-analyzer-backend.onrender.com/](https://password-security-analyzer-backend.onrender.com/)
- **Repository**: [https://github.com/SuvajitDey2003/password-security-analyzer/](https://github.com/SuvajitDey2003/password-security-analyzer/)

## ✨ Features

### Security Analysis
- **🔍 Real-time Analysis**: Instant password strength evaluation as you type (with smart debouncing)
- **📊 Entropy Calculation**: Shannon entropy-based password complexity measurement
- **🚨 Breach Detection**: Checks against Have I Been Pwned API using k-anonymity for privacy
- **📖 Dictionary Check**: Validates against common password databases
- **🔎 Pattern Detection**: Identifies:
  - Repeated characters (e.g., "aaa", "111")
  - Sequential numbers (e.g., "123", "987")
  - Sequential letters (e.g., "abc", "xyz")
  - Keyboard patterns (e.g., "qwerty", "asdf")
  - Repeating patterns (e.g., "abcabc")

### User Experience
- **🎯 Visual Strength Indicator**: Color-coded strength bar (Red/Orange/Green)
- **📋 Detailed Feedback**: Actionable security recommendations
- **🔒 Privacy First**: Show/hide password toggle
- **⚡ Rate Limiting**: Prevents API abuse (30 requests/minute per IP)
- **🌐 CORS Support**: Secure cross-origin resource sharing

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Next.js Frontend (React 19)                │   │
│  │  • User Interface (page.js)                          │   │
│  │  • API Integration (lib/api.js)                      │   │
│  │  • Real-time Validation with Debouncing              │   │
│  │  • Visual Feedback Components                        │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS
                              │ POST /analyze-password
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              FastAPI Main Application                │   │
│  │  • CORS Middleware                                   │   │
│  │  • Request/Response Validation (Pydantic)            │   │
│  │  • Health Check Endpoint (/)                         │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     ROUTING LAYER                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              API Routes (routes.py)                  │   │
│  │  • Rate Limiter (30 req/min per IP)                  │   │
│  │  • Error Handling                                    │   │
│  │  • Request Routing                                   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   BUSINESS LOGIC LAYER                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │          Password Analyzer (analyze.py)              │   │
│  │  • Orchestrates all security checks                  │   │
│  │  • Scoring algorithm                                 │   │
│  │  • Strength classification                           │   │
│  └──────────────────────────────────────────────────────┘   │
│                              │                               │
│         ┌────────────────────┼────────────────────┐          │
│         ▼                    ▼                    ▼          │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐   │
│  │  Entropy    │     │  Patterns   │     │ Dictionary  │   │
│  │  Calculator │     │  Detector   │     │  Checker    │   │
│  │ (entropy.py)│     │(patterns.py)│     │(dictionary  │   │
│  │             │     │             │     │    .py)     │   │
│  └─────────────┘     └─────────────┘     └─────────────┘   │
│         │                                         │          │
│         │                    ┌────────────────────┘          │
│         │                    ▼                               │
│         │            ┌─────────────┐                         │
│         │            │Breach Check │                         │
│         │            │(breach_check│                         │
│         │            │    .py)     │                         │
│         │            └─────────────┘                         │
│         │                    │                               │
└─────────┼────────────────────┼───────────────────────────────┘
          │                    │
          ▼                    ▼
┌──────────────────┐  ┌──────────────────────────────┐
│  Math Library    │  │    External API Layer        │
│  (Shannon        │  │  ┌────────────────────────┐  │
│   Entropy)       │  │  │ Have I Been Pwned API  │  │
│                  │  │  │ (k-anonymity search)   │  │
└──────────────────┘  │  └────────────────────────┘  │
                      └──────────────────────────────┘
```

### Architecture Components

#### Frontend (Next.js)
- **Framework**: Next.js 16 with React 19
- **Features**:
  - Client-side rendering with hooks (`useState`, `useEffect`)
  - Smart debouncing (1.2s) for API calls
  - Responsive UI with visual feedback
  - Real-time password validation (min 6 characters)

#### Backend (FastAPI)
- **Framework**: FastAPI with Uvicorn server
- **Core Modules**:
  - `entropy.py`: Shannon entropy calculation based on character set
  - `patterns.py`: Pattern detection using regex and sequence matching
  - `dictionary.py`: Common password database lookup
  - `breach_check.py`: HIBP API integration with k-anonymity
  - `rate_limiter.py`: IP-based request throttling
  - `analyze.py`: Main orchestration and scoring engine

#### Data Flow
1. User enters password in frontend
2. Debounced API call to `/analyze-password` endpoint
3. Rate limiter validates request
4. Parallel security checks:
   - Entropy calculation
   - Pattern detection
   - Dictionary lookup
   - Breach check (HIBP API)
5. Scoring algorithm applies penalties for security issues
6. Response with strength, score, entropy, issues, and breach count
7. Frontend displays results with visual indicators

## 🛠️ Tech Stack

### Backend
- **Python 3.x** - Programming language
- **FastAPI** - Modern web framework for building APIs
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation and settings management
- **Requests** - HTTP library for API calls
- **Have I Been Pwned API** - Breach detection service

### Frontend
- **Next.js 16.1.1** - React framework with server-side rendering
- **React 19.2.3** - UI library
- **JavaScript (ES6+)** - Programming language

### Deployment
- **Vercel** - Frontend hosting
- **Render** - Backend hosting

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 18 or higher
- npm or yarn

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/SuvajitDey2003/password-security-analyzer.git
cd password-security-analyzer/backend
```

2. **Create and activate virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the backend server**
```bash
# Using uvicorn directly
uvicorn backend.app.main:app --reload

# Or using the start script
chmod +x start.sh
./start.sh
```

The backend API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd password-security-analyzer/frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Update API URL for local development** (Optional)

Edit `frontend/lib/api.js` and uncomment the local URL:
```javascript
const API_URL = "http://localhost:8000/analyze-password";
// const API_URL = "https://password-security-analyzer-backend.onrender.com/analyze-password";
```

4. **Run the development server**
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 🚀 Usage

### Using the Web Interface

1. Open the application in your browser
2. Enter a password in the input field (minimum 6 characters)
3. Toggle "Show password" to view your input
4. View real-time analysis results:
   - **Strength bar**: Visual indicator (Red/Orange/Green)
   - **Score**: Numerical rating (0-100)
   - **Entropy**: Password complexity in bits
   - **Breach count**: Number of times found in data breaches
   - **Issues**: List of security concerns

### API Usage

#### Endpoint: `POST /analyze-password`

**Request:**
```bash
curl -X POST https://password-security-analyzer-backend.onrender.com/analyze-password \
  -H "Content-Type: application/json" \
  -d '{"password": "YourPassword123!"}'
```

**Response:**
```json
{
  "score": 65,
  "entropy": 59.54,
  "strength": "Moderate",
  "issues": [
    "Sequential numbers detected"
  ],
  "breach_count": 0
}
```

**Response Fields:**
- `score` (int): Security score from 0-100
- `entropy` (float): Shannon entropy in bits
- `strength` (string): "Weak", "Moderate", or "Strong"
- `issues` (array): List of detected security issues
- `breach_count` (int): Number of times password appeared in breaches

**Rate Limits:**
- 30 requests per minute per IP address
- Returns HTTP 429 when exceeded

## 📁 Project Structure

```
password-security-analyzer/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes.py           # API endpoints and rate limiting
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── analyze.py          # Main password analysis orchestrator
│   │   │   ├── entropy.py          # Shannon entropy calculation
│   │   │   ├── patterns.py         # Pattern detection logic
│   │   │   ├── dictionary.py       # Common password checking
│   │   │   ├── breach_check.py     # HIBP API integration
│   │   │   └── rate_limiter.py     # Request rate limiting
│   │   └── models/
│   │       ├── __init__.py
│   │       └── schemas.py          # Pydantic models
│   ├── data/
│   │   └── common_passwords.sample.txt  # Sample password dictionary
│   ├── tests/                      # Unit tests
│   │   ├── test_analyze.py
│   │   ├── test_breach_check.py
│   │   ├── test_dictionary.py
│   │   ├── test_entropy.py
│   │   └── test_patterns.py
│   ├── requirements.txt            # Python dependencies
│   └── start.sh                    # Backend startup script
├── frontend/
│   ├── app/
│   │   ├── layout.js               # Root layout component
│   │   ├── page.js                 # Main page component
│   │   └── globals.css             # Global styles
│   ├── lib/
│   │   └── api.js                  # API client
│   ├── public/                     # Static assets
│   ├── package.json                # Node.js dependencies
│   └── next.config.mjs             # Next.js configuration
├── .gitignore
└── README.md
```

## 🔒 Security Features

### Privacy Protection
- **K-Anonymity**: Passwords are never sent to HIBP in full; only the first 5 characters of the SHA-1 hash are transmitted
- **Client-side Hashing**: Hash matching occurs locally in the backend
- **No Storage**: Passwords are not logged or stored anywhere

### Rate Limiting
- IP-based throttling (30 requests/minute)
- Prevents brute-force enumeration
- Configurable window and limits

### Breach Detection
- Integration with Have I Been Pwned (HIBP) database
- 600+ million compromised passwords
- Updated regularly with new breaches

### Scoring Algorithm
The password score (0-100) is calculated based on:
- Base score from entropy (2x entropy value, capped at 100)
- Penalties:
  - Low entropy (<40 bits): -20 points
  - Pattern detection: -15 points
  - Repeated characters/patterns: -40 points
  - Common dictionary password: -30 points
  - Found in breaches: -40 points

## 🧪 Testing

### Backend Tests

Run the test suite:
```bash
cd backend
pytest tests/
```

Test coverage includes:
- Entropy calculation
- Pattern detection
- Dictionary checking
- Breach API integration
- End-to-end analysis

### Manual Testing

Test the API directly:
```bash
# Health check
curl http://localhost:8000/

# Analyze a password
curl -X POST http://localhost:8000/analyze-password \
  -H "Content-Type: application/json" \
  -d '{"password": "TestPassword123"}'
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint for JavaScript/React code
- Write unit tests for new features
- Update documentation as needed
- Keep commits atomic and descriptive

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Suvajit Dey**
- GitHub: [@SuvajitDey2003](https://github.com/SuvajitDey2003)
- Project: [Password Security Analyzer](https://github.com/SuvajitDey2003/password-security-analyzer)

## 🙏 Acknowledgments

- [Have I Been Pwned](https://haveibeenpwned.com/) for the breach detection API
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [Next.js](https://nextjs.org/) for the React framework
- [Vercel](https://vercel.com/) and [Render](https://render.com/) for hosting services

## 📊 Future Enhancements

- [ ] Password generation feature
- [ ] Multi-language support
- [ ] Password strength history tracking
- [ ] Browser extension
- [ ] Mobile application
- [ ] Advanced pattern detection (leetspeak, substitutions)
- [ ] Customizable password policies
- [ ] Export analysis reports

---

**⚠️ Disclaimer**: This tool is for educational and informational purposes. Always use unique, strong passwords and enable multi-factor authentication for sensitive accounts.
