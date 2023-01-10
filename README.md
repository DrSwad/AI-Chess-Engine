# AI Chess Engine

An AI-driven implementation of a chess engine comparing multiple AI strategies including Minimax, MCTS, Neural network and simulating head-to-head games between different strategies.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/DrSwad/Chess-Engine-with-AI-Strategies.git
cd chess_engine_with_ai_strategies
```

2. Create and activate virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m simulations.<simulation-name>
```

## Unit Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```
