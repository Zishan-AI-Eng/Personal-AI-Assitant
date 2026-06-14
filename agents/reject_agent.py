def process_reject(user_query: str = "") -> str:
    """
    A highly optimized, zero-latency guardrail response.
    Bypasses the LLM entirely to save cost and inference time.
    """
    return (
        "I must respectfully decline this request. As the official AI Assistant for Zeeshan Khan's portfolio, "
        "my scope is strictly limited to discussing his professional experience, skills, and AI engineering projects. "
        "Would you like to hear about his recent work with Agentic Workflows or his AI tech stack?"
    )