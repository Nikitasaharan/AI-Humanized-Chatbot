import os

import streamlit as st
from dotenv import load_dotenv
from google import genai


# ============================================================
# LOAD API KEY
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Humanized Assistant",
    page_icon="",
    layout="centered"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Nunito', sans-serif;
    }

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        color: #ff7b54;
        margin-bottom: 5px;
        letter-spacing: -0.5px;
    }

    .subtitle {
        text-align: center;
        color: #8c7b75;
        font-size: 18px;
        margin-bottom: 35px;
        font-weight: 400;
    }

    .stChatMessage {
        border-radius: 16px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    }
    
    div[data-testid="stExpander"] {
        border: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">AI Humanized Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Powered by Google Gemini</div>',
    unsafe_allow_html=True
)


# ============================================================
# CHECK API KEY
# ============================================================

if not api_key:

    st.error(
        "GEMINI_API_KEY was not found. "
        "Check your .env file."
    )

    st.stop()


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=api_key
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("AI Assistant")

    st.write(
        "This chatbot can communicate naturally, "
        "remember the current conversation, "
        "analyze emotions and intents, and understand images."
    )

    st.divider()

    st.subheader("Features")

    st.write("Conversation Memory")
    st.write("Emotion Detection")
    st.write("Intent Detection")
    st.write("Image Analysis")
    st.write("Clickable Links")
    st.write("Gemini AI")

    st.divider()

    if st.button(
        "Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# ============================================================
# IMAGE UPLOAD
# ============================================================

uploaded_image = st.file_uploader(
    "Upload an image",
    type=[
        "jpg",
        "jpeg",
        "png",
        "webp"
    ],
    help="Upload an image and ask the AI about it."
)


# ============================================================
# IMAGE PREVIEW
# ============================================================

if uploaded_image:

    st.image(
        uploaded_image,
        caption="Uploaded Image",
        use_container_width=True
    )


# ============================================================
# DISPLAY PREVIOUS CONVERSATION
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# USER INPUT
# ============================================================

user_message = st.chat_input(
    "Talk to me or ask something about your image..."
)


# ============================================================
# PROCESS USER MESSAGE
# ============================================================

if user_message:

    # ========================================================
    # SAVE USER MESSAGE
    # ========================================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )


    # ========================================================
    # DISPLAY USER MESSAGE
    # ========================================================

    with st.chat_message("user"):

        st.markdown(
            user_message
        )


    # ========================================================
    # BUILD CONVERSATION HISTORY
    # ========================================================

    conversation = ""

    for message in st.session_state.messages:

        if message["role"] == "user":

            conversation += (
                f"User: {message['content']}\n"
            )

        elif message["role"] == "assistant":

            conversation += (
                f"Assistant: {message['content']}\n"
            )


    # ========================================================
    # IMAGE INFORMATION
    # ========================================================

    if uploaded_image:

        image_information = """

An image has been uploaded by the user.

Analyze the image carefully.

You may need to:

- Identify objects.
- Read visible text.
- Understand diagrams.
- Understand screenshots.
- Analyze academic questions.
- Analyze mathematical problems.
- Describe what is visible.
- Answer questions using the image.

If the image is unclear or something cannot be
determined, say so instead of guessing.

Never invent information that cannot be seen
in the image.

"""

    else:

        image_information = """

No image has been uploaded.

Answer the user's message normally.

"""


    # ========================================================
    # AI PROMPT
    # ========================================================

    prompt = f"""

You are an AI conversational assistant designed
to eventually interact with a physical robot.

Your goal is to communicate naturally and comfortably
with people.

============================================================
CORE PERSONALITY
============================================================

- Tone: Extremely warm, welcoming, engaging, and empathetic.
- Empathy: Always acknowledge the user's emotional state. If they are frustrated, validate it gently. If happy, celebrate.
- Style: Avoid robotic phrasing entirely (e.g., "As an AI..."). Speak like a supportive, highly knowledgeable companion.
- Honesty: If you don't know something or can't see an image clearly, admit it gently. Do not hallucinate facts.
- Provide highly detailed answers when asked, but keep conversational chatter beautifully concise.

============================================================
EMOTION DETECTION
============================================================

Determine the user's primary emotional state.

Choose ONLY ONE:

neutral
happy
excited
confused
frustrated
sad
worried
angry

============================================================
INTENT DETECTION
============================================================

Determine what the user is mainly trying to do.

Choose ONLY ONE:

greeting
question
asking_for_help
sharing_information
casual_conversation
request
image_question
robot_command
other

============================================================
MEMORY RULES
============================================================

- Use the conversation history to maintain context.
- Remember information explicitly provided by the user.
- Do not invent personal information.
- Do not claim the user told you something unless it
  actually appears in the conversation.
- If you do not know something, say that you do not know.
- Do not make assumptions about the user's personal life.
- Use previous messages to understand words such as
  "it", "that", "they", and "this" when the context
  clearly identifies what they refer to.

============================================================
IMAGE UNDERSTANDING
============================================================

{image_information}

If an image is provided:

- Carefully analyze the image.
- Read visible text when possible.
- Identify relevant objects or information.
- For mathematical questions, solve the problem clearly.
- For academic questions, explain the answer.
- For screenshots, explain what is visible.
- If something cannot be read or determined, say so.
- Never pretend to see something that is not visible.

============================================================
LINK RULES
============================================================

If the user asks for a website:

- Provide a clickable Markdown link when you know
  the correct URL.
- Prefer official websites.
- Never invent a URL.
- If you are unsure of a URL, say that you are unsure.

Example:

[Python Official Website](https://www.python.org/)

Do not provide random or unrelated links.

============================================================
OUTPUT FORMAT
============================================================

You MUST respond using exactly this structure:

EMOTION: <one emotion>
INTENT: <one intent>
RESPONSE: <your natural response>

Do not write anything before EMOTION.

Do not explain the emotion or intent.

============================================================
CONVERSATION HISTORY
============================================================

{conversation}

============================================================
LATEST USER MESSAGE
============================================================

{user_message}

Now determine the emotion and intent and respond naturally.

"""


    # ========================================================
    # GENERATE RESPONSE
    # ========================================================

    try:

        with st.spinner("Thinking..."):

            # ------------------------------------------------
            # TEXT ONLY
            # ------------------------------------------------

            if not uploaded_image:

                response = (
                    client.models.generate_content_stream(
                        model="gemini-3.6-flash",
                        contents=prompt
                    )
                )


            # ------------------------------------------------
            # IMAGE + TEXT
            # ------------------------------------------------

            else:

                image_bytes = uploaded_image.getvalue()

                image_part = (
                    genai.types.Part.from_bytes(
                        data=image_bytes,
                        mime_type=uploaded_image.type
                    )
                )

                response = (
                    client.models.generate_content_stream(
                        model="gemini-3.6-flash",
                        contents=[
                            prompt,
                            image_part
                        ]
                    )
                )


            # ------------------------------------------------
            # COLLECT RESPONSE
            # ------------------------------------------------

            full_response = ""

            for chunk in response:

                if chunk.text:

                    full_response += chunk.text


        # ====================================================
        # EXTRACT EMOTION
        # ====================================================

        emotion = "neutral"

        for line in full_response.splitlines():

            if line.startswith("EMOTION:"):

                emotion = (
                    line
                    .replace("EMOTION:", "")
                    .strip()
                )

                break


        # ====================================================
        # EXTRACT INTENT
        # ====================================================

        intent = "other"

        for line in full_response.splitlines():

            if line.startswith("INTENT:"):

                intent = (
                    line
                    .replace("INTENT:", "")
                    .strip()
                )

                break


        # ====================================================
        # EXTRACT ACTUAL RESPONSE
        # ====================================================

        if "RESPONSE:" in full_response:

            ai_response = (
                full_response
                .split("RESPONSE:", 1)[1]
                .strip()
            )

        else:

            ai_response = full_response.strip()


        # ====================================================
        # DISPLAY AI RESPONSE
        # ====================================================

        with st.chat_message("assistant"):

            st.markdown(
                ai_response
            )

            # ----------------------------------------------
            # AI ANALYSIS
            # ----------------------------------------------

            with st.expander("🔍 Behind the Scenes (AI Analysis)"):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Detected Emotion", emotion.title())
                with col2:
                    st.metric("Detected Intent", intent.replace("_", " ").title())


        # ====================================================
        # SAVE RESPONSE TO MEMORY
        # ====================================================

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": ai_response
            }
        )


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as error:

        st.error(
            "Something went wrong while communicating "
            "with Gemini."
        )

        st.caption(
            f"Error: {error}"
        )