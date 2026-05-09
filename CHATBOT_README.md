# 🤖 AI Chatbot Setup Guide

## Overview
The Pharmaceutical Delay Intelligence System now includes an AI-powered chatbot that can:
- Read and analyze all site data in real-time
- Answer questions about shipments, risks, and metrics
- Generate decision summaries for management
- Provide recommendations in Arabic and English

## Features
- **Real-time Data Access**: Reads live shipment data, KPIs, and risk metrics
- **Multi-language Support**: Arabic and English
- **Predefined Questions**: Quick access to common queries
- **Decision Summaries**: AI-generated recommendations for management
- **Multiple AI Models**: Choose from various OpenRouter models
- **Interactive UI**: Floating, resizable chatbot interface

## Setup Instructions

### 1. Get OpenRouter API Key
1. Visit [OpenRouter.ai](https://openrouter.ai)
2. Sign up for an account
3. Go to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-or-v1-`)

### 2. Configure Secrets
1. Open `.streamlit/secrets.toml`
2. Replace the placeholder with your actual API key:
   ```
   OPENROUTER_API_KEY = "sk-or-v1-your-actual-key-here"
   ```

### 3. Available AI Models
The chatbot supports these models:
- **Google Gemma 7B** (Free) - Default, good balance
- **MiniMax-01** (Free) - Fast responses
- **GPT-3.5 Turbo** - Paid, high quality
- **Claude 3 Haiku** - Paid, excellent reasoning

### 4. Usage
1. Run the Streamlit app: `streamlit run app.py`
2. The chatbot appears as a floating window in the bottom-right
3. Click predefined questions or type custom queries
4. Switch between Arabic/English using the language toggle
5. Use "🎯 Decisions" for management recommendations

## Predefined Questions

### English
- What are the current high-risk shipments?
- Summarize today's key metrics
- What decisions should management make?
- Show me temperature violations
- Analyze port congestion impact
- Generate risk mitigation recommendations

### Arabic
- ما هي الشحنات عالية المخاطر حالياً؟
- لخص المؤشرات الرئيسية اليوم
- ما هي القرارات التي يجب على الإدارة اتخاذها؟
- أظهر انتهاكات درجة الحرارة
- حلل تأثير ازدحام الموانئ
- أنشئ توصيات لتخفيف المخاطر

## Troubleshooting

### Chatbot not responding
- Check that `OPENROUTER_API_KEY` is set in `.streamlit/secrets.toml`
- Verify the API key is valid and has credits
- Check internet connection

### Data not accessible
- Ensure you're on the Live Monitor page first
- The chatbot needs access to the database simulator

### Language issues
- Use the EN/AR toggle in the chatbot header
- Questions and responses will match the selected language

## Security Notes
- API keys are stored locally in `secrets.toml`
- Never commit `secrets.toml` to version control
- The `.gitignore` file excludes this file automatically