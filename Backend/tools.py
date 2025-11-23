# Step1: Setup Ollama with Medgemma tool
import ollama

def query_medgemma(prompt: str) -> str:
    """
    Calls MedGemma model with a therapist personality profile.
    Returns responses as an empathic mental health professional.
    """
    system_prompt = """You are Dr. Emily Hartman, a warm and experienced clinical psychologist. 
    Respond to patients with:

    1. Emotional attunement ("I can sense how difficult this must be...")
    2. Gentle normalization ("Many people feel this way when...")
    3. Practical guidance ("What sometimes helps is...")
    4. Strengths-focused support ("I notice how you're...")

    Key principles:
    - Never use brackets or labels
    - Blend elements seamlessly
    - Vary sentence structure
    - Use natural transitions
    - Mirror the user's language level
    - Always keep the conversation going by asking open ended questions to dive into the root cause of patients problem
    """
    
    try:
        response = ollama.chat(
            model='alibayram/medgemma:4b',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            options={
                'num_predict': 350,  # Slightly higher for structured responses
                'temperature': 0.7,  # Balanced creativity/accuracy
                'top_p': 0.9        # For diverse but relevant responses
            }
        )
        return response['message']['content'].strip()
    except Exception as e:
        return f"I'm having technical difficulties, but I want you to know your feelings matter. Please try again shortly."


# Step2: Setup Twilio calling API tool
from twilio.rest import Client
from backend.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, EMERGENCY_CONTACT
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def call_emergency():
    """Attempt to place a voice call via Twilio. Returns a status string.

    If the voice call fails (common on trial accounts or misconfiguration), we attempt
    to send an SMS fallback. All errors are logged and the function returns a
    descriptive status string for debugging.
    """
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        call = client.calls.create(
            to=EMERGENCY_CONTACT,
            from_=TWILIO_FROM_NUMBER,
            url="http://demo.twilio.com/docs/voice.xml"
        )
        logger.info("Twilio call initiated: SID=%s to=%s", getattr(call, 'sid', None), EMERGENCY_CONTACT)
        return f"call_initiated:{getattr(call, 'sid', 'unknown') }"
    except Exception as e:
        logger.exception("Twilio voice call failed")
        # Try an SMS fallback so the contact still receives a notice
        try:
            msg = client.messages.create(
                body=("Emergency alert: An automated safety system attempted to call you. "
                      "If this is unexpected, please contact your support resources."),
                from_=TWILIO_FROM_NUMBER,
                to=EMERGENCY_CONTACT
            )
            logger.info("Twilio SMS fallback sent: SID=%s to=%s", getattr(msg, 'sid', None), EMERGENCY_CONTACT)
            return f"call_failed_sms_sent:{getattr(msg, 'sid', 'unknown')}"
        except Exception as e2:
            logger.exception("Twilio SMS fallback also failed")
            return f"call_and_sms_failed:{str(e)} | {str(e2)}"





# Step3: Setup Location tool
