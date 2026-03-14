## 🎥 Project Demo
[![Watch the Demo](Thumbnail.png)](https://drive.google.com/file/d/1CKU3IE29Z7zkkgnAR_WN0UoNo0g43Q8U/view?usp=sharing)

# NyayaSetu ⚖️
**AI-Powered Legal Intelligence for the Indian Judiciary**

NyayaSetu is a cutting-edge platform designed to demystify the Indian legal system through advanced AI analysis. It provides citizens and legal professionals with data-driven insights, outcome predictions, and structured legal guidance.

---

## 🌟 Key Features

- **Intuitive Intake Wizard**: A seamless, multi-step process to gather case details without legal jargon.
- **Nyaya Bento-Box Dashboard**: A sophisticated, modern interface for visualizing case metrics, strengths, and predictions.
- **AI Analysis Engine**:
    - **Outcome Prediction**: Predictive modeling to estimate the likely success of a case.
    - **Case Strength Analyzer**: Deep analysis of case facts to identify key advantages and vulnerabilities.
    - **Timeline Forecast**: Estimating potential durations based on case complexity and court load.
    - **Legal Similarity Engine**: Identifying relevant precedents and similar historical cases.
- **Automated Document Generation**: One-click generation of customized legal checklists and summaries in PDF format.
- **Premium Aesthetics**: A state-of-the-art UI featuring glassmorphism, dark mode support, and interactive visualizations.

---

## 🛠️ Technology Stack

### Frontend
- **Framework**: React 19 (via Vite)
- **Styling**: Vanilla CSS with modern Design Tokens & Glassmorphism
- **Navigation**: React Router 7
- **Visualization**: Chart.js
- **API Client**: Axios

### Backend
- **Framework**: FastAPI (Python)
- **WebServer**: Uvicorn
- **PDF Core**: ReportLab
- **Logging**: Structured industry-standard logging

### AI & Intelligence
- **Natural Language Processing**: Custom embedding models and LLM integrations for case analysis.
- **Logic**: Modular AI services for prediction and explanation generation.

---

## 📂 Project Structure

```text
Nyaya-setu/
├── backend/                # FastAPI Backend Application
│   ├── ai/                 # AI Core (Predictors, Analyzers, Similarity)
│   ├── routes/             # RESTful API Endpoints
│   ├── services/           # Supporting Business Logic
│   ├── dataset/            # Data assets for models
│   └── main.py             # Application Entry Point
├── frontend/               # React Frontend Application
│   ├── src/
│   │   ├── components/     # Reusable UI Components
│   │   ├── pages/          # Full-Page Views
│   │   ├── context/        # Global State (Theme, Data)
│   │   └── services/       # API Integration Layer
│   └── vite.config.js      # Build Configuration
└── models/                 # Pre-trained models & large assets
```

---

## 🚀 Getting Started

### Prerequisites
- **Python**: 3.9 or higher
- **Node.js**: 18.x or higher
- **Package Manager**: npm or yarn

### Backend Installation
1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Installation
1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Launch development server:
   ```bash
   npm run dev
   ```

---

## 📋 API Reference

The backend provides an interactive API playground:
- **Swagger Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check**: `GET /health`

---

## 🤝 Contributing

Contributions are welcome! Please ensure you follow the existing design system for UI changes and provide docstrings for any new backend services.

## 📄 License

This project is licensed under the MIT License.

---
Built for the **Advanced Agentic Coding** initiative.
