import streamlit as st
import pickle
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SMS Guard | Spam Classifier",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background: #F4F7FC;
}
header {visibility: hidden;}

.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

.hero {
    background: linear-gradient(120deg,#101B32,#243F68);
    padding: 35px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 36px;
    color: white;
    margin-bottom: 8px;
}

.hero p {
    color: #D2DDED;
    font-size: 16px;
}

.metric-card {
    background: white;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #E3E9F2;
    box-shadow: 0 3px 12px rgba(20,40,70,.05);
}

.metric-label {
    color: #68758A;
    font-size: 14px;
}

.metric-value {
    color: #172B4D;
    font-size: 29px;
    font-weight: bold;
}

.result-spam {
    background: #FFF0EF;
    border: 1px solid #F2B8B4;
    border-radius: 15px;
    padding: 25px;
    color: #B42318;
    text-align: center;
}

.result-ham {
    background: #EAF8F0;
    border: 1px solid #A8DFC0;
    border-radius: 15px;
    padding: 25px;
    color: #167344;
    text-align: center;
}

.stButton button {
    border-radius: 9px;
    min-height: 45px;
    font-weight: 600;
}

footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    with open("spam_model.pkl", "rb") as f:
        return pickle.load(f)

try:
    model = load_model()
except Exception as e:
    st.error(f"Could not load spam_model.pkl: {e}")
    st.stop()

# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if "message" not in st.session_state:
    st.session_state.message = ""

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("🛡️ SMS GUARD")
    st.caption("Machine Learning Security")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        ["Dashboard", "Detection History", "About Project"]
    )

    st.divider()

    st.success("Model loaded successfully")
    st.caption("Version 1.0 | Python + Streamlit")

# ---------------- DASHBOARD ----------------
if page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>🛡️ SMS Spam Classifier</h1>
        <p>Intelligent SMS detection powered by Machine Learning</p>
        <p>Analyze suspicious messages and protect your inbox.</p>
    </div>
    """, unsafe_allow_html=True)

    # Metrics
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-label">MODEL ACCURACY</div>
        <div class="metric-value">96.62%</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-label">TOTAL MESSAGES</div>
        <div class="metric-value">5,169</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-label">SPAM MESSAGES</div>
        <div class="metric-value">653</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    st.subheader("🔍 Analyze Your Message")
    st.write("Enter or paste an SMS message below.")

    message = st.text_area(
        "SMS Message",
        value=st.session_state.message,
        height=150,
        placeholder="Example: Congratulations! You won a free prize..."
    )

    col1, col2 = st.columns(2)

    with col1:
        detect = st.button(
            "🔍 Detect Message",
            type="primary",
            use_container_width=True
        )

    with col2:
        clear = st.button(
            "🗑️ Clear Input",
            use_container_width=True
        )

    if clear:
        st.session_state.message = ""
        st.rerun()

    if detect:
        if not message.strip():
            st.warning("Please enter a message first.")

        else:
            try:
                prediction = model.predict([message])[0]
                result = str(prediction).strip().lower()

                if result == "spam":
                    st.markdown(f"""
                    <div class="result-spam">
                        <h2>🚨 SPAM MESSAGE DETECTED</h2>
                        <p>This message has been classified as spam.</p>
                        <h3>⚠️ Be careful before responding or clicking links.</h3>
                    </div>
                    """, unsafe_allow_html=True)

                elif result in ["ham", "not spam", "not_spam"]:
                    st.markdown("""
                    <div class="result-ham">
                        <h2>✅ NOT SPAM</h2>
                        <p>This message has been classified as legitimate.</p>
                        <h3>✔ No spam detected by the model.</h3>
                    </div>
                    """, unsafe_allow_html=True)

                else:
                    st.warning(f"Unexpected model prediction: {prediction}")
                    st.stop()

                st.session_state.history.insert(0, {
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "message": message,
                    "result": result.upper()
                })

            except Exception as e:
                st.error(f"Prediction error: {e}")

    st.divider()

    st.subheader("💡 Try Sample Messages")

    samples = [
        "Congratulations! You won a free iPhone. Claim now!",
        "Hello, I will meet you at college tomorrow.",
        "URGENT! You have won a cash prize. Call now!",
    ]

    for i, sample in enumerate(samples):
        if st.button(f"Try Example {i+1}", key=f"sample_{i}"):
            st.session_state.message = sample
            st.rerun()

# ---------------- HISTORY ----------------
elif page == "Detection History":

    st.title("📊 Detection History")
    st.write("Previously analyzed messages.")

    if st.session_state.history:
        for item in st.session_state.history:
            with st.container(border=True):
                st.caption(item["time"])
                st.write(item["message"])

                if item["result"] == "SPAM":
                    st.error("🚨 SPAM")
                else:
                    st.success("✅ NOT SPAM")

        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()

    else:
        st.info("No messages analyzed yet.")

# ---------------- ABOUT ----------------
elif page == "About Project":

    st.title("📘 About SMS Guard")

    st.write("""
    SMS Guard is a machine-learning-based SMS spam detection system.

    **Technologies used:**
    - Python
    - Streamlit
    - Pandas
    - Scikit-learn
    - TF-IDF Vectorization
    - Multinomial Naive Bayes

    **Dataset:**
    Kaggle SMS Spam Collection Dataset.

    **Objective:**
    To classify SMS messages into Spam and Ham
    categories using Natural Language Processing.
    """)

    st.info("Developed as a Machine Learning academic project.")