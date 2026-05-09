import streamlit as st
import requests
import json
from datetime import datetime
import time

class PharmaChatbot:
    def __init__(self):
        self.api_key = st.secrets.get("OPENROUTER_API_KEY", "")
        self.base_url = "https://openrouter.ai/api/v1"

        # Available models
        self.models = {
            "minimax/minimax-01": "MiniMax-01 (Free)",
            "google/gemma-7b-it": "Gemma 7B (Free)",
            "openai/gpt-3.5-turbo": "GPT-3.5 Turbo",
            "anthropic/claude-3-haiku": "Claude 3 Haiku"
        }

        # Predefined questions in both languages
        self.predefined_questions = {
            "en": [
                "What are the current high-risk shipments?",
                "Summarize today's key metrics",
                "What decisions should management make?",
                "Show me temperature violations",
                "Analyze port congestion impact",
                "Generate risk mitigation recommendations",
                "What are the top risk factors?",
                "Show shipment status overview"
            ],
            "ar": [
                "ما هي الشحنات عالية المخاطر حالياً؟",
                "لخص المؤشرات الرئيسية اليوم",
                "ما هي القرارات التي يجب على الإدارة اتخاذها؟",
                "أظهر انتهاكات درجة الحرارة",
                "حلل تأثير ازدحام الموانئ",
                "أنشئ توصيات لتخفيف المخاطر",
                "ما هي أهم عوامل المخاطر؟",
                "أظهر نظرة عامة على حالة الشحنات"
            ]
        }

    def get_site_content(self):
        """Extract current site data for context"""
        try:
            # Get data from session state or generate sample
            if 'db_simulator' in st.session_state:
                db_simulator = st.session_state.db_simulator
                active_shipments = db_simulator.get_active_shipments()
                high_risk = db_simulator.get_high_risk_shipments()

                content = f"""
                Current Active Shipments: {len(active_shipments)}
                High Risk Shipments: {len(high_risk)}

                Active Shipments Data:
                {active_shipments.to_string() if len(active_shipments) > 0 else 'No active shipments'}

                High Risk Shipments:
                {high_risk.to_string() if len(high_risk) > 0 else 'No high risk shipments'}

                Current KPIs:
                - Total Shipments: {len(active_shipments)}
                - High Risk: {len(high_risk)}
                - Risk Percentage: {len(high_risk)/len(active_shipments)*100:.1f}% if active_shipments else 0
                """
                return content
            else:
                return "Site data not available. Please navigate to Live Monitor page first."
        except Exception as e:
            return f"Error extracting site content: {str(e)}"

    def generate_decision_summary(self, content):
        """Generate decision recommendations based on current data"""
        prompt = f"""
        Based on the following pharmaceutical supply chain data, provide a concise summary of key decisions that management should make:

        {content}

        Focus on:
        1. Immediate actions for high-risk shipments
        2. Preventive measures
        3. Resource allocation recommendations
        4. Monitoring priorities

        Keep the response actionable and specific.
        """

        return self.call_openrouter(prompt)

    def call_openrouter(self, prompt, model="google/gemma-7b-it"):
        """Call OpenRouter API"""
        if not self.api_key:
            return """❌ **OpenRouter API Key Required**

To use the AI chatbot, you need to:

1. **Get a FREE API key** from [OpenRouter.ai](https://openrouter.ai/keys)
2. **Add it to** `.streamlit/secrets.toml`:
   ```
   OPENROUTER_API_KEY = "sk-or-v1-your-actual-key-here"
   ```
3. **Restart the Streamlit app**

The chatbot will then be fully functional! 🤖"""

        # Check if it's a test key
        if self.api_key == "sk-or-v1-test-key-for-development":
            return """❌ **Test API Key Detected**

You're using a test key. To enable the chatbot:

1. **Visit** [OpenRouter.ai](https://openrouter.ai/keys)
2. **Sign up** (it's free!)
3. **Create an API key**
4. **Replace the test key** in `.streamlit/secrets.toml`
5. **Restart the app**

Get your real API key now! 🔑"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            elif response.status_code == 401:
                return """❌ **Invalid API Key**

Your OpenRouter API key is not valid. Please:

1. **Check your key** at [OpenRouter.ai/keys](https://openrouter.ai/keys)
2. **Ensure it's copied correctly** (should start with `sk-or-v1-`)
3. **Update** `.streamlit/secrets.toml` with the correct key
4. **Restart** the Streamlit app

Need help? Visit the [CHATBOT_README.md](CHATBOT_README.md) file."""
            elif response.status_code == 429:
                return "❌ **Rate Limit Exceeded**\n\nYou've made too many requests. Please wait a moment and try again."
            elif response.status_code == 402:
                return "❌ **Insufficient Credits**\n\nYour OpenRouter account needs more credits. Visit [OpenRouter.ai](https://openrouter.ai) to top up."
            else:
                return f"❌ **API Error**: {response.status_code}\n\n{response.text}"

        except requests.exceptions.ConnectionError:
            return "❌ **Connection Error**\n\nUnable to connect to OpenRouter. Check your internet connection."
        except requests.exceptions.Timeout:
            return "❌ **Timeout Error**\n\nRequest timed out. Please try again."
        except Exception as e:
            return f"❌ **Unexpected Error**: {str(e)}"

    def render_chatbot(self):
        """Render the interactive chatbot component"""

        # Chatbot container with glassmorphism
        st.markdown("""
            <style>
            .chatbot-container {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 400px;
                height: 600px;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                z-index: 1000;
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }

            .chatbot-header {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 15px;
                border-radius: 20px 20px 0 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
                cursor: move;
            }

            .chatbot-messages {
                flex: 1;
                padding: 15px;
                overflow-y: auto;
                background: rgba(0, 0, 0, 0.1);
            }

            .chatbot-input {
                padding: 15px;
                background: rgba(255, 255, 255, 0.05);
                border-top: 1px solid rgba(255, 255, 255, 0.1);
            }

            .message {
                margin-bottom: 10px;
                padding: 10px;
                border-radius: 10px;
                max-width: 80%;
            }

            .message.user {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                margin-left: auto;
                text-align: right;
            }

            .message.bot {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }

            .minimize-btn {
                background: none;
                border: none;
                color: white;
                font-size: 18px;
                cursor: pointer;
                padding: 0;
            }

            .predefined-questions {
                display: flex;
                flex-wrap: wrap;
                gap: 5px;
                margin-bottom: 10px;
            }

            .question-btn {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                padding: 5px 10px;
                border-radius: 15px;
                cursor: pointer;
                font-size: 12px;
                transition: all 0.3s;
            }

            .question-btn:hover {
                background: rgba(255, 255, 255, 0.2);
                transform: translateY(-1px);
            }
            </style>
        """, unsafe_allow_html=True)

        # Initialize session state for chatbot
        if 'chatbot_minimized' not in st.session_state:
            st.session_state.chatbot_minimized = False
        if 'chat_messages' not in st.session_state:
            st.session_state.chat_messages = []
        if 'selected_model' not in st.session_state:
            st.session_state.selected_model = "google/gemma-7b-it"
        if 'chat_language' not in st.session_state:
            st.session_state.chat_language = "en"

        # Chatbot toggle button (when minimized)
        if st.session_state.chatbot_minimized:
            if st.button("💬 Chat Assistant", key="chat_toggle", help="Open AI Assistant"):
                st.session_state.chatbot_minimized = False
                st.rerun()
            return

        # Main chatbot container
        with st.container():
            col1, col2, col3 = st.columns([1, 3, 1])

            with col1:
                if st.button("🔽", key="minimize_chat", help="Minimize chatbot"):
                    st.session_state.chatbot_minimized = True
                    st.rerun()

            with col2:
                st.markdown("""
                    <div style="text-align: center; color: white; font-weight: bold;">
                        🤖 AI Assistant
                    </div>
                """, unsafe_allow_html=True)

            with col3:
                # Language toggle
                lang_options = ["EN", "AR"]
                current_lang = "EN" if st.session_state.chat_language == "en" else "AR"
                if st.button(current_lang, key="lang_toggle", help="Switch language"):
                    st.session_state.chat_language = "ar" if st.session_state.chat_language == "en" else "en"
                    st.rerun()

        # Model selection
        selected_model_display = st.selectbox(
            "AI Model:",
            options=list(self.models.keys()),
            format_func=lambda x: self.models[x],
            key="model_selector",
            index=list(self.models.keys()).index(st.session_state.selected_model)
        )
        st.session_state.selected_model = selected_model_display

        # Messages container
        st.markdown('<div class="chatbot-messages">', unsafe_allow_html=True)

        # Show welcome/setup message if no API key or test key
        if not self.api_key or self.api_key == "sk-or-v1-test-key-for-development":
            st.markdown("""
                <div class="message bot">
                    <strong>Welcome to Pharma AI Assistant! 🤖</strong><br>
                    To start chatting, you need to set up your OpenRouter API key.<br>
                    <strong>Click "Setup Guide" below to learn how! 📚</strong>
                </div>
            """, unsafe_allow_html=True)

        # Display chat messages
        for msg in st.session_state.chat_messages[-10:]:  # Show last 10 messages
            msg_class = "user" if msg["role"] == "user" else "bot"
            st.markdown(f"""
                <div class="message {msg_class}">
                    <strong>{msg['timestamp']}</strong><br>
                    {msg['content']}
                </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Predefined questions
        lang = st.session_state.chat_language
        questions = self.predefined_questions.get(lang, self.predefined_questions["en"])

        st.markdown(f'<div class="predefined-questions">', unsafe_allow_html=True)
        cols = st.columns(2)
        for i, question in enumerate(questions[:8]):  # Show first 8 questions
            with cols[i % 2]:
                if st.button(question, key=f"q_{i}", help=f"Ask: {question}"):
                    self.add_message("user", question)
                    self.process_question(question)
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Custom input
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_input(
                "Ask me anything about the data...",
                key="chat_input",
                placeholder="Type your question here..."
            )

            col1, col2 = st.columns([4, 1])
            with col1:
                submitted = st.form_submit_button("📤 Send")
            with col2:
                if st.form_submit_button("🎯 Decisions"):
                    self.generate_decisions_summary()
                    st.rerun()

            if submitted and user_input.strip():
                self.add_message("user", user_input.strip())
                self.process_question(user_input.strip())
                st.rerun()

        # Setup help button
        if st.button("📚 Setup Guide", key="setup_guide", help="Get help setting up the chatbot"):
            st.markdown("""
            ### 🤖 Chatbot Setup Instructions

            **To enable the AI chatbot, follow these steps:**

            1. **Visit OpenRouter**: Go to [openrouter.ai](https://openrouter.ai)
            2. **Sign up** for a free account
            3. **Navigate to API Keys**: Click on your profile → API Keys
            4. **Create new key**: Generate a new API key
            5. **Copy the key**: It should look like `sk-or-v1-xxxxx...`

            6. **Update secrets file**: Open `.streamlit/secrets.toml` and replace:
               ```
               # Remove the comment and add your real key:
               OPENROUTER_API_KEY = "sk-or-v1-your-actual-key-here"
               ```

            7. **Restart the app**: Close and reopen Streamlit

            **That's it!** The chatbot will be fully functional. 🎉

            **Need more help?** Check `CHATBOT_README.md` for detailed instructions.
            """)
            return

    def add_message(self, role, content):
        """Add message to chat history"""
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.chat_messages.append({
            "role": role,
            "content": content,
            "timestamp": timestamp
        })

    def process_question(self, question):
        """Process user question and generate response"""
        site_content = self.get_site_content()

        # Create context-aware prompt
        prompt = f"""
        You are an AI assistant for a pharmaceutical supply chain monitoring system.
        Answer the user's question based on this current site data:

        {site_content}

        User Question: {question}

        Provide a helpful, accurate response in the same language as the question.
        If the question is in Arabic, respond in Arabic. If in English, respond in English.
        """

        response = self.call_openrouter(prompt, st.session_state.selected_model)
        self.add_message("bot", response)

    def generate_decisions_summary(self):
        """Generate and display decision summary"""
        site_content = self.get_site_content()

        prompt = f"""
        Based on this pharmaceutical supply chain data, provide a comprehensive summary of decisions that management should make:

        {site_content}

        Structure your response as:
        1. 🚨 IMMEDIATE ACTIONS (for high-risk situations)
        2. 📊 MONITORING PRIORITIES (what to watch closely)
        3. 🛠️ PREVENTIVE MEASURES (long-term improvements)
        4. 📈 RESOURCE ALLOCATION (where to focus efforts)

        Be specific and actionable. Respond in the current language: {'Arabic' if st.session_state.chat_language == 'ar' else 'English'}
        """

        response = self.call_openrouter(prompt, st.session_state.selected_model)
        self.add_message("bot", f"📋 **Decision Summary**\n\n{response}")