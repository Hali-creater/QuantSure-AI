# AI Trade Prediction & Confirmation Agent

A professional AI agent for market analysis and trade confirmation, powered by OpenAI's GPT-4o. This agent follows institutional-grade analysis frameworks, including Smart Money Concepts (SMC), to provide objective market insights.

## Features

- **Objective Analysis:** Evaluates market context, structure, liquidity, and technical confirmations.
- **Probability-Based:** Expresses confidence levels instead of guaranteed predictions.
- **Risk Management:** Recommends logical stop-losses, take-profits, and risk-to-reward ratios.
- **Strict Response Format:** Ensures consistent and professional reporting.
- **Supports Multiple Markets:** Stocks, Indices, Forex, and Crypto.

## Project Structure

- `agent.py`: Contains the `TradeAgent` class for interacting with the OpenAI API.
- `prompt.py`: Stores the comprehensive system prompt that defines the agent's behavior.
- `main.py`: CLI application for running the agent.
- `test_agent.py`: Unit tests for ensuring reliability.
- `requirements.txt`: Project dependencies.

## Setup

1. **Clone the repository.**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment Variables:**
   Copy `.env.example` to `.env` and add your OpenAI API Key:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and replace `your_api_key_here` with your actual key.

## Usage

Run the CLI tool:
```bash
python main.py
```
Paste your market data (e.g., price levels, RSI values, trend descriptions) and type `DONE` on a new line to receive the analysis.

## Testing

Run unit tests to verify the core logic:
```bash
python3 test_agent.py
```

## Disclaimer

This AI agent is a decision-support system and **not** a financial advisor. Trading involves significant risk. Never trade more than you can afford to lose.
