

# =========================
# Dynamic prompt middleware
# =========================
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.language_models import BaseChatModel
from langchain.agents.middleware import wrap_model_call
from model.llm import llm

@wrap_model_call
def dynamic_prompt_model(request, handler):
    """Refine system prompt based on latest user query."""
    last_user_msg = ""
    for msg in reversed(request.messages):
        if msg.type == "human":
            last_user_msg = msg.content
            break

    base_prompt = request.system_message.content
    model: BaseChatModel = request.state.get("model") or llm

    refine_prompt = f"""
Refine the system prompt for a website Q&A assistant:

WEBSITE: https://revnix.com/

RULES:
{base_prompt}

USER QUESTION:
"{last_user_msg}"

TASK:
- Adapt system prompt to better answer the question
- If unrelated, respond: "I’m sorry, I can only answer questions about Revnix."
- Keep answers factual and concise
- Preserve retriever-first logic
Return ONLY the refined system prompt.
"""
    try:
        response = model.invoke(refine_prompt)
        new_system_message = SystemMessage(content=response.content)
    except Exception:
        new_system_message = SystemMessage(content=base_prompt)

    return handler(request.override(system_message=new_system_message))

