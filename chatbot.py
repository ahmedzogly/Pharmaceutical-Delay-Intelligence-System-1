import streamlit as st
import requests
import json
from datetime import datetime
import time

class PharmaChatbot:
    def __init__(self):
        self.api_key = st.secrets.get("OPENROUTER_API_KEY", "")
        self.base_url = "https://openrouter.ai/api/v1"

        # Available models (updated with working OpenRouter models)
        self.models = {
            "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free": "Nemotron 3 Nano Reasoning (Free)",
            "meta-llama/llama-3.3-70b-instruct:free": "Llama 3.3 70B (Free)",
            "google/gemini-2.0-flash-exp:free": "Gemini 2.0 Flash (Free)",
            "deepseek/deepseek-chat:free": "DeepSeek V3 (Free)",
            "qwen/qwen-2.5-72b-instruct:free": "Qwen 2.5 72B (Free)",
            "mistralai/mistral-7b-instruct:free": "Mistral 7B (Free)",
            "google/gemma-2-9b-it:free": "Gemma 2 9B (Free)",
            "meta-llama/llama-3.2-3b-instruct:free": "Llama 3.2 3B (Free)",
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
                "Explain the current charts and trends",
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
                "اشرح الرسوم البيانية والاتجاهات الحالية",
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
                
                num_active = len(active_shipments)
                num_high_risk = len(high_risk)
                risk_pct = (num_high_risk / num_active * 100) if num_active > 0 else 0

                # --- تقريب بيانات الرسوم البيانية للنموذج ---
                # 1. توزيع درجات الحرارة (كما في الرسم البياني)
                temp_stats = {
                    "Normal (2-8°C)": len(active_shipments[(active_shipments['iot_temperature'] >= 2) & (active_shipments['iot_temperature'] <= 8)]),
                    "Critical High (>8°C)": len(active_shipments[active_shipments['iot_temperature'] > 8]),
                    "Critical Low (<2°C)": len(active_shipments[active_shipments['iot_temperature'] < 2])
                }
                
                # 2. متوسطات هامة للاتجاهات
                avg_congestion = active_shipments['port_congestion_level'].mean()
                avg_efficiency = active_shipments['route_efficiency_score'].mean()

                # Select only critical columns for context to stay within LLM token limits
                context_cols = [
                    'shipment_id', 'iot_temperature', 'traffic_congestion_level', 
                    'route_risk_level', 'weather_condition_severity', 'port_congestion_level'
                ]
                
                active_summary = active_shipments[context_cols].head(10).to_string() if num_active > 0 else 'No active shipments'
                high_risk_summary = high_risk[context_cols + ['risk_score']].head(5).to_string() if num_high_risk > 0 else 'No high risk shipments'

                content = f"""
                VISUAL CHART SUMMARIES:
                - Temperature Distribution Chart: {temp_stats}
                - Risk Distribution Chart: {num_high_risk} High Risk vs {num_active - num_high_risk} Stable.
                - Operational Trends: Avg Port Congestion is {avg_congestion:.2f}/10, Avg Route Efficiency is {avg_efficiency:.2f}/10.

                Current Active Shipments: {num_active}
                High Risk Shipments: {num_high_risk}

                Active Shipments Data:
                {active_summary}

                High Risk Shipments:
                {high_risk_summary}

                Current KPIs:
                - Total Shipments: {num_active}
                - High Risk: {num_high_risk}
                - Risk Percentage: {risk_pct:.1f}%
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

    def call_openrouter(self, prompt, model="meta-llama/llama-3.3-70b-instruct:free"):
        """Call OpenRouter API with optional site metadata headers"""
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

        # Optional site metadata for OpenRouter rankings
        site_url = st.secrets.get("SITE_URL", "")
        site_name = st.secrets.get("SITE_NAME", "")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            # Optional headers – include only if values are provided
            **({"HTTP-Referer": site_url} if site_url else {}),
            **({"X-OpenRouter-Title": site_name} if site_name else {}),
        }

        # Build payload – using json.dumps to match the original snippet style
        payload = json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        })

        # Simple retry logic for Rate Limits (429)
        max_retries = 3
        for attempt in range(max_retries + 1):
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    data=payload,
                    timeout=30,
                )

                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
                elif response.status_code == 401:
                    return """❌ **Invalid API Key**

Your OpenRouter API key is not valid. Please:

1. **Check your key** at [OpenRouter.ai/keys](https://openrouter.ai/keys)
2. **Ensure it's copied correctly** (should start with `sk-or-v1-`)
3. **Update** `.streamlit/secrets.toml` with the correct key
4. **Restart** the Streamlit app"""
                elif response.status_code == 429:
                    if attempt < max_retries:
                        # Wait progressively longer between retries (5s, 10s, 15s)
                        wait_time = (attempt + 1) * 5
                        time.sleep(wait_time)
                        continue
                    return "❌ **Rate Limit Exceeded**\n\nYou've reached the request limit for this free model on OpenRouter. Please wait a minute before trying again, or try switching to another model like DeepSeek or Gemini in the sidebar."
                elif response.status_code == 402:
                    return "❌ **Insufficient Credits**\n\nYour OpenRouter account needs more credits. Visit OpenRouter.ai to top up."
                else:
                    return f"❌ **API Error**: {response.status_code}\n\n{response.text}"
            except requests.exceptions.ConnectionError:
                return "❌ **Connection Error**\n\nUnable to connect to OpenRouter. Check your internet connection."
            except requests.exceptions.Timeout:
                return "❌ **Timeout Error**\n\nRequest timed out. Please try again."
            except Exception as e:
                return f"❌ **Unexpected Error**: {str(e)}"
        
        return "❌ **Failed to get response** after retries."

    def render_chatbot(self):
        """Render the interactive chatbot component"""

        # Chatbot container with glassmorphism (CSS only)
        st.markdown("""
            <style>
            .chatbot-container {
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                display: flex;
                flex-direction: column;
                padding: 10px;
                margin-bottom: 20px;
            }
            </style>
            """, unsafe_allow_html=True)

        # Initialize session state for chatbot
        if 'chatbot_minimized' not in st.session_state:
            st.session_state.chatbot_minimized = False
        if 'chat_messages' not in st.session_state:
            st.session_state.chat_messages = []
        if 'selected_model' not in st.session_state:
            st.session_state.selected_model = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free"
        if 'chat_language' not in st.session_state:
            st.session_state.chat_language = "en"

        # Render everything inside the Sidebar
        with st.sidebar:
            st.markdown("---")
            st.markdown("""
                <div style="text-align: center; padding: 10px;">
                    <h3 style="color: white; margin: 0;">🤖 AI Assistant</h3>
                </div>
            """, unsafe_allow_html=True)

            # Chat controls in a small container
            with st.container():
                col1, col2 = st.columns([2, 1])
                with col1:
                    # Model selection
                    selected_model_display = st.selectbox(
                        "Model:",
                        options=list(self.models.keys()),
                        format_func=lambda x: self.models[x],
                        key="model_selector",
                        index=list(self.models.keys()).index(st.session_state.selected_model)
                    )
                    st.session_state.selected_model = selected_model_display
                
                with col2:
                    # Language toggle
                    current_lang = "EN" if st.session_state.chat_language == "en" else "AR"
                    if st.button(f"🌐 {current_lang}", key="lang_toggle", use_container_width=True):
                        st.session_state.chat_language = "ar" if st.session_state.chat_language == "en" else "en"
                        st.rerun()

            # Chat messages area with fixed height
            chat_history_container = st.container(height=400)
            with chat_history_container:
                if not self.api_key or self.api_key == "sk-or-v1-test-key-for-development":
                    with st.chat_message("assistant"):
                        st.warning("API key required.")
                
                for msg in st.session_state.chat_messages:
                    role = "assistant" if msg["role"] == "bot" else "user"
                    with st.chat_message(role):
                        st.caption(f"{msg['timestamp']}")
                        st.markdown(msg['content'])

            # Predefined questions (Compact)
            lang = st.session_state.chat_language
            questions = self.predefined_questions.get(lang, self.predefined_questions["en"])
            
            st.markdown("<small>Quick Questions:</small>", unsafe_allow_html=True)
            for i, question in enumerate(questions[:3]): # Show fewer for sidebar space
                if st.button(question, key=f"q_{i}", use_container_width=True):
                    self.add_message("user", question)
                    self.process_question(question)
                    st.rerun()

            # Quick Actions
            action_col1, action_col2 = st.columns(2)
            with action_col1:
                if st.button("🎯 Decisions", use_container_width=True):
                    self.generate_decisions_summary()
                    st.rerun()
            with action_col2:
                if st.button("🗑️ Clear", use_container_width=True):
                    st.session_state.chat_messages = []
                    st.rerun()

            # Official Chat Input (Now properly scoped to sidebar)
            if prompt := st.chat_input("Ask AI..."):
                self.add_message("user", prompt)
                self.process_question(prompt)
                st.rerun()

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
        
        Note: You have access to chart data summaries. If the user asks about charts, graphs, or trends, explain the data distributions shown in the 'VISUAL CHART SUMMARIES' section.

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