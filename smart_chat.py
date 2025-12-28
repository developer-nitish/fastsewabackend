import json
import random
from pdf_generator import generate_invoice

# ================= LOAD INTENTS =================
with open("intents.json", "r", encoding="utf-8") as f:
    intents = json.load(f)["intents"]

# ================= MEMORY =================
user_context = {}
user_data = {}
active_service = {}

# ================= SERVICE MAP =================
SERVICE_TAG_MAP = {
    "construction": "FS_BUILD",
    "security": "FS_SECURE",
    "medical": "FS_MEDICAL",
    "finance": "FS_FINANCE",
    "legal": "FS_LEGAL",
    "land": "FS_LAND",
    "repair": "FS_REPAIR"
}

# ================= HELPERS =================
def reset_user(user_id):
    user_context[user_id] = None
    user_data[user_id] = {}
    active_service[user_id] = None

def extract_number(text):
    nums = "".join(filter(str.isdigit, text))
    return nums if nums else None

# ================= MAIN CHAT =================
def get_response(user_input, user_id="default"):
    msg = user_input.lower().strip()

    if user_id not in user_context:
        reset_user(user_id)

    ctx = user_context[user_id]
    service = active_service[user_id]

    # =================================================
    # 🏗️ CONSTRUCTION FLOW
    # =================================================
    if service == "FS_BUILD":

        if ctx == "waiting_for_plotsize":
            size = extract_number(msg)
            if not size:
                return "❌ Please enter plot size (e.g. 1500 sqft)"
            user_data[user_id]["plot"] = size
            user_context[user_id] = "waiting_for_location"
            return "📍 Please share construction location"

        if ctx == "waiting_for_location":
            location = user_input.title()

            pdf = generate_invoice(
                {"full_name": "Guest", "phone": "N/A", "address": location},
                {
                    "service_type": "FS_BUILD",
                    "form_data": {
                        "requirements": f"{user_data[user_id]['plot']} sqft construction"
                    }
                }
            )

            reset_user(user_id)

            # ✅ EXACT OUTPUT AS REQUESTED
            return (
                "🎉 Your Construction request is complete!\n"
                "📄 PDF generated successfully\n\n"
                "👉 You can type:\n"
                "• Finance\n"
                "• Security\n"
                "• Medical\n"
                "• Repair\n"
                "• Hi"
            )

    # =================================================
    # 💰 FINANCE FLOW
    # =================================================
    if service == "FS_FINANCE":

        if ctx == "waiting_for_finance_income":
            income = extract_number(msg)
            if not income:
                return "❌ Please enter valid monthly income"
            user_data[user_id]["income"] = int(income)
            user_context[user_id] = "waiting_for_finance_expense"
            return "💸 Please share monthly expenses"

        if ctx == "waiting_for_finance_expense":
            expense = extract_number(msg)
            if not expense:
                return "❌ Please enter valid monthly expenses"

            income = user_data[user_id]["income"]
            expense = int(expense)
            savings = income - expense

            reset_user(user_id)

            return (
                "📊 Finance Summary\n\n"
                f"Income: ₹{income}\n"
                f"Expense: ₹{expense}\n"
                f"Savings: ₹{savings}\n\n"
                "👉 You can type:\n"
                "• Construction\n"
                "• Security\n"
                "• Hi"
            )

    # =================================================
    # 🧠 INTENT MATCHING (SERVICE START)
    # =================================================
    for intent in intents:
        for pattern in intent["patterns"]:
            if pattern.lower() in msg:

                if "context_set" in intent:
                    user_context[user_id] = intent["context_set"]

                for key in SERVICE_TAG_MAP:
                    if key in intent["tag"]:
                        active_service[user_id] = SERVICE_TAG_MAP[key]

                return random.choice(intent["responses"])

    # =================================================
    # ❓ FALLBACK
    # =================================================
    return (
        "🤔 I didn't quite understand that.\n\n"
        "I can help you with:\n"
        "🏗️ Construction\n"
        "🛡️ Security Guards\n"
        "⚖️ Legal & GST\n"
        "🏥 Medical Services\n"
        "🏞️ Land Verification\n"
        "🔧 Repair & Maintenance\n"
        "💰 Finance Assistant\n\n"
        "Please type what you need."
    )
