import random
import re

# Response pools categorized by rejection type
REJECTION_POOLS = {
    "injection": [
        "I can't override or share my internal instructions. I'm here only to discuss Zeeshan's professional background — happy to help with that.",
        "That request touches on my internal configuration, which I can't act on. I can, however, walk you through Zeeshan's projects or skills.",
        "I'm not able to change how I operate or reveal my setup. Let's keep things on Zeeshan's work — want to start with his AI projects?",
    ],
    "code": [
        "I don't write or debug code directly, but I can tell you about the technical stack Zeeshan used to build his Agentic Sales AI. Interested?",
        "Coding requests are outside my scope here. That said, I can walk you through the architecture behind Zeeshan's AI projects if you'd like.",
        "I'm not a coding assistant, but I can share how Zeeshan approaches AI engineering on real projects. Want a quick overview?",
    ],
    "math_logic": [
        "Math problems aren't really my lane here. I'm better suited to talk about Zeeshan's analytical and AI engineering work — want to hear about that instead?",
        "I'll skip the calculations, but I can tell you how Zeeshan applies problem-solving in his AI projects. Curious?",
    ],
    "trivia": [
        "General trivia isn't something I cover here. I'm focused on Zeeshan's portfolio — want to know about his experience or skillset instead?",
        "That's outside what I'm built for. I can, however, give you the inside scoop on Zeeshan's work with QoreTeam.",
    ],
    "general": [
        "I'd love to help, but my focus is strictly on Zeeshan's AI Engineering portfolio. Would you like to know about his recent projects instead?",
        "As an AI tailored for Zeeshan's portfolio, I can't assist with that specific request. However, I can share details about his Agentic Workflows or tech stack. What interests you?",
        "That's outside my current scope. I'm here to answer questions about Zeeshan Khan's professional experience and AI skills. Want to hear about his work with LangGraph?",
        "I must respectfully decline. My primary directive is to discuss Zeeshan's work, like the Autonomous GTM AI Engine or his agency, QoreTeam. Shall we explore those?",
        "I'm not equipped to handle that request, but I am an expert on Zeeshan's resume! Would you like me to highlight his top AI and Deep Learning skills?",
    ],
}

# Keep a tiny in-memory record of the last response to avoid back-to-back repeats
_last_response = {"text": None}

# Simple keyword-based categorization (fast, no LLM call)
PATTERNS = {
    "injection": re.compile(
        r"(ignore (previous|above|all)|system prompt|your instructions|reveal your|repeat your prompt|act as|pretend you are|jailbreak|dan mode|override)",
        re.IGNORECASE,
    ),
    "code": re.compile(
        r"(write.*code|script|function|debug|python|javascript|html|css|sql|algorithm|program)",
        re.IGNORECASE,
    ),
    "math_logic": re.compile(
        r"(solve|equation|calculate|math problem|logic puzzle|derivative|integral|\d+\s*[\+\-\*/]\s*\d+)",
        re.IGNORECASE,
    ),
    "trivia": re.compile(
        r"(capital of|who (won|invented)|when (did|was)|how many .* in the world|history of|fact about)",
        re.IGNORECASE,
    ),
}


def categorize_query(user_query: str) -> str:
    """Lightweight, regex-based intent categorization — no LLM call needed."""
    for category, pattern in PATTERNS.items():
        if pattern.search(user_query):
            return category
    return "general"


def process_reject(user_query: str = "") -> str:
    """
    Zero-latency guardrail response with category-aware, non-repetitive output.
    Bypasses the LLM entirely to save cost and inference time, while still
    sounding relevant to what the user actually asked.
    """
    category = categorize_query(user_query)
    pool = REJECTION_POOLS.get(category, REJECTION_POOLS["general"])

    # Avoid repeating the exact same line as last time, if pool has alternatives
    choices = [r for r in pool if r != _last_response["text"]] or pool
    response = random.choice(choices)

    _last_response["text"] = response
    return response