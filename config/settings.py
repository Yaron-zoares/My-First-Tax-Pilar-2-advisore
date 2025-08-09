"""
Pilar2 Configuration Settings
Configuration settings for Pilar2 system
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    APP_NAME: str = "Pilar2"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Pilar2 Financial Analysis System"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # Database Configuration
    DATABASE_URL: Optional[str] = None
    
    # File Upload Configuration
    UPLOAD_DIR: Path = BASE_DIR / "data" / "uploads"
    PROCESSED_DIR: Path = BASE_DIR / "data" / "processed"
    REPORTS_DIR: Path = BASE_DIR / "reports"
    
    # Maximum file upload size (50MB)
    MAX_FILE_SIZE: int = 50 * 1024 * 1024
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS: dict = {
        'excel': ['.xlsx', '.xls'],
        'pdf': ['.pdf'],
        'csv': ['.csv']
    }
    
    # AI Model Configuration
    MODEL_DIR: Path = BASE_DIR / "models"
    NLP_MODEL_PATH: Path = MODEL_DIR / "nlp" / "qa_model"
    CLASSIFICATION_MODEL_PATH: Path = MODEL_DIR / "classification" / "classifier"
    
    # External APIs
    OPENAI_API_KEY: Optional[str] = None
    AZURE_OPENAI_KEY: Optional[str] = None
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    SERPER_API_KEY: Optional[str] = None
    
    # Email Configuration
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # Cloud Storage Configuration
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: Optional[str] = None
    S3_BUCKET: Optional[str] = None
    AZURE_STORAGE_CONNECTION_STRING: Optional[str] = None
    AZURE_STORAGE_CONTAINER: Optional[str] = None
    GOOGLE_CLOUD_PROJECT: Optional[str] = None
    GOOGLE_CLOUD_BUCKET: Optional[str] = None
    
    # Token Configuration
    REFRESH_TOKEN_EXPIRE_DAYS: Optional[str] = None
    
    # Tax Rates Configuration
    CORPORATE_TAX_RATE: Optional[str] = None
    PERSONAL_TAX_RATE: Optional[str] = None
    VAT_RATE: Optional[str] = None
    
    # Model Configuration
    MODEL_CACHE_TTL: Optional[str] = None
    MAX_TOKENS: Optional[str] = None
    TEMPERATURE: Optional[str] = None
    
    # CORS and Hosts Configuration
    CORS_ORIGINS: Optional[str] = None
    ALLOWED_HOSTS: Optional[str] = None
    
    # Monitoring Configuration
    SENTRY_DSN: Optional[str] = None
    NEW_RELIC_LICENSE_KEY: Optional[str] = None
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",  # React frontend
        "http://localhost:8501",  # Streamlit frontend
        "http://localhost:8000",  # FastAPI docs
    ]
    
    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Path = BASE_DIR / "logs" / "pilar2.log"
    
    # Tax Calculation Settings
    TAX_RATES: dict = {
        'corporate': 0.23,  # 23% corporate tax rate
        'personal': 0.31,   # 31% personal tax rate
        'vat': 0.17,        # 17% VAT rate
    }
    
    # Regulatory Settings
    GIR_XML_VERSION: str = "1.0"
    REPORTING_PERIOD: str = "annual"
    
    # Cache Configuration
    CACHE_TTL: int = 3600  # 1 hour
    REDIS_URL: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Allow extra fields from .env file

# Create settings instance
settings = Settings()

# Ensure directories exist
def create_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        settings.UPLOAD_DIR,
        settings.PROCESSED_DIR,
        settings.REPORTS_DIR / "xml",
        settings.REPORTS_DIR / "pdf", 
        settings.REPORTS_DIR / "word",
        settings.MODEL_DIR / "nlp",
        settings.MODEL_DIR / "classification",
        settings.MODEL_DIR / "recommendations",
        BASE_DIR / "logs"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# Initialize directories
create_directories()

# English text constants
ENGLISH_TEXTS = {
    'app_title': 'Pilar2 - Financial Report Analysis System',
    'upload_success': 'File uploaded successfully',
    'upload_error': 'Error uploading file',
    'processing': 'Processing data...',
    'analysis_complete': 'Analysis completed successfully',
    'report_generated': 'Report generated successfully',
    'error_occurred': 'An error occurred',
    'no_file_selected': 'No file selected',
    'invalid_file_type': 'Unsupported file type',
    'file_too_large': 'File too large',
    'tax_calculations': 'Tax calculations',
    'adjustments': 'Adjustments',
    'regulatory_reports': 'Regulatory reports',
    'financial_analysis': 'Financial analysis',
    'ai_qa': 'Smart Q&A',
    'recommendations': 'Recommendations',
    'settings': 'Settings',
    'help': 'Help',
    'about': 'About',
}

# Hebrew text constants
HEBREW_TEXTS = {
    'app_title': 'Pilar2 - מערכת ניתוח דוחות פיננסיים',
    'upload_success': 'הקובץ הועלה בהצלחה',
    'upload_error': 'שגיאה בהעלאת הקובץ',
    'processing': 'מעבד נתונים...',
    'analysis_complete': 'הניתוח הושלם בהצלחה',
    'report_generated': 'הדוח נוצר בהצלחה',
    'error_occurred': 'אירעה שגיאה',
    'no_file_selected': 'לא נבחר קובץ',
    'invalid_file_type': 'סוג קובץ לא נתמך',
    'file_too_large': 'הקובץ גדול מדי',
    'tax_calculations': 'חישובי מס',
    'adjustments': 'התאמות',
    'regulatory_reports': 'דוחות רגולטוריים',
    'financial_analysis': 'ניתוח פיננסי',
    'ai_qa': 'שאלות ותשובות חכמות',
    'recommendations': 'המלצות',
    'settings': 'הגדרות',
    'help': 'עזרה',
    'about': 'אודות',
}

# Financial categories for classification
FINANCIAL_CATEGORIES = {
    'revenue': {
        'en': 'Revenue',
        'subcategories': ['sales', 'services', 'other_income']
    },
    'expenses': {
        'en': 'Expenses', 
        'subcategories': ['cost_of_goods', 'operating_expenses', 'financial_expenses']
    },
    'assets': {
        'en': 'Assets',
        'subcategories': ['current_assets', 'fixed_assets', 'intangible_assets']
    },
    'liabilities': {
        'en': 'Liabilities',
        'subcategories': ['current_liabilities', 'long_term_liabilities']
    },
    'equity': {
        'en': 'Equity',
        'subcategories': ['share_capital', 'retained_earnings', 'other_equity']
    }
}

# Tax adjustment categories
TAX_ADJUSTMENTS = {
    'depreciation': {
        'en': 'Depreciation',
        'description': 'Depreciation for tax purposes'
    },
    'provisions': {
        'en': 'Provisions', 
        'description': 'Provisions for tax purposes'
    },
    'capital_gains': {
        'en': 'Capital Gains',
        'description': 'Capital gains and losses'
    },
    'foreign_income': {
        'en': 'Foreign Income',
        'description': 'Income from outside Israel'
    },
    'loss_carryforward': {
        'en': 'Loss Carryforward',
        'description': 'Losses from previous years'
    }
}
