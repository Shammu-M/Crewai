"""CrewAI application service for manager-led banking conversations."""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import StructuredTool
from dotenv import load_dotenv
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from models.mcp_tools import accounts_mcp, services_mcp, transactions_mcp

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

DEMO_USER_ID = "DEMO-USER-001"
DEMO_ACCOUNT_ID = "ACCT-1001"
MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b").strip()
MAX_RPM = 900


def _is_rate_limit_error(error: BaseException) -> bool:
    text = str(error).lower()
    return "429" in text or "rate limit" in text or "too many requests" in text


@retry(retry=retry_if_exception(_is_rate_limit_error), wait=wait_exponential(multiplier=1, min=2, max=30), stop=stop_after_attempt(4), reraise=True)
def create_llm() -> ChatGroq:
    """Create the Groq client for the free-tier OpenAI open-weight model."""
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing. Add it to the project .env file.")
    return ChatGroq(
        model=MODEL_NAME,
        groq_api_key=api_key,
        temperature=0.1,
        max_tokens=1200,
    )


def build_crew() -> Crew:
    from crewai import Agent, Crew, Process, Task

    llm = create_llm()
    accounts_tool = StructuredTool.from_function(func=accounts_mcp, name="accounts_mcp", description="Query demo account balances, types, and profiles.")
    transactions_tool = StructuredTool.from_function(func=transactions_mcp, name="transactions_mcp", description="Query demo transaction history and spending.")
    services_tool = StructuredTool.from_function(func=services_mcp, name="services_mcp", description="Query demo customer service requests.")
    accounts_agent = Agent(
        role="Account Details Specialist",
        goal="Retrieve accurate account facts for the supplied demo user and account.",
        backstory="You operate the mocked Accounts MCP endpoint. Return only tool-grounded facts.",
        tools=[accounts_tool], llm=llm, allow_delegation=False, verbose=False,
    )
    transactions_agent = Agent(
        role="Transaction and Statement Specialist",
        goal="Retrieve transaction facts and spending patterns for the supplied demo user and account.",
        backstory="You operate the mocked Transactions MCP endpoint. Return dates, amounts, and categories from the tool.",
        tools=[transactions_tool], llm=llm, allow_delegation=False, verbose=False,
    )
    service_agent = Agent(
        role="Customer Service Specialist",
        goal="Find address, cheque book, and KYC request status for the supplied demo user.",
        backstory="You operate the mocked Services MCP endpoint. Never claim that a real request was submitted.",
        tools=[services_tool], llm=llm, allow_delegation=False, verbose=False,
    )
    coordinator = Agent(
        role="Banking Operations Manager",
        goal="Delegate the request to the appropriate specialists and synthesize a factual answer.",
        backstory="You coordinate specialists. Use the supplied identifiers, preserve tool output, and never invent banking data.",
        llm=llm, allow_delegation=True, verbose=False,
    )
    request_task = Task(
        description=(
        "Handle the banking request below. Delegate to one or more specialists as needed.\n\n"
        "User ID: {user_id}\n"
        "Primary account ID: {account_id}\n"
        "Customer request: {user_prompt}\n\n"
        "Specialists must query their MCP tool using the supplied identifiers or request topic. "
        "The final response must summarize tool results, include relevant dates and amounts, "
        "say when no record exists, and never claim a real-world action was completed."
        ),
        expected_output=(
        "A concise answer with: result summary, relevant account or transaction details, "
        "service-request status when applicable, and a clear note when data is unavailable."
        ),
    )
    return Crew(
        agents=[accounts_agent, transactions_agent, service_agent],
        tasks=[request_task],
        process=Process.hierarchical,
        manager_agent=coordinator,
        max_rpm=MAX_RPM,
        verbose=False,
    )


@retry(retry=retry_if_exception(_is_rate_limit_error), wait=wait_exponential(multiplier=1, min=2, max=45), stop=stop_after_attempt(4), reraise=True)
def answer_banking_request(user_prompt: str) -> str:
    user_prompt = user_prompt.strip()
    if not user_prompt:
        return "Please enter a banking question."
    time.sleep(0.15)
    specialist_outputs = {
        "accounts": accounts_mcp(DEMO_ACCOUNT_ID),
        "transactions": transactions_mcp(DEMO_ACCOUNT_ID),
        "service_requests": services_mcp(user_prompt),
    }
    context = "\n\n".join(
        f"{name.upper()} SPECIALIST OUTPUT:\n{output}"
        for name, output in specialist_outputs.items()
    )
    response = create_llm().invoke(
        [
            SystemMessage(
                content=(
                    "You are the Banking Operations Manager. Answer only from the supplied "
                    "specialist outputs. The user is a demo user, not a real bank customer. "
                    "Be concise, mention account IDs and dates when relevant, and never claim "
                    "that a real-world service request was submitted. If the data does not "
                    "answer the question, say so clearly."
                )
            ),
            HumanMessage(
                content=(
                    f"User ID: {DEMO_USER_ID}\n"
                    f"Primary account: {DEMO_ACCOUNT_ID}\n"
                    f"Customer request: {user_prompt}\n\n{context}"
                )
            ),
        ]
    )
    return str(response.content)
