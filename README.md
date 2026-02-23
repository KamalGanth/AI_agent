# AI Agent — Streamlit Chat

Professional summary

AI Agent is a lightweight Streamlit web application that exposes a small collection of tools (calculator, unit converter, math solver, and news fetcher) powered by a Google Generative AI model (Gemini) orchestrated via `langchain` / `langgraph`. The app provides a chat-style UI to interact with the model and invoke domain-specific tools.

Repository contents

- `main.py` — Core agent and tool implementations.
- `UI.py` — Streamlit front-end and chat interface.
- `test.py` — Simple test/demo for the `recent_news` helper.
- `requirements.txt` — Locked Python dependencies used to run the app.
- `Dockerfile` — Container recipe to build and run the Streamlit service.

Highlights

- Small, modular toolset: calculator, unit converter (`pint`), symbolic math (`sympy`), and external news fetcher.
- Streaming agent responses to the UI for a responsive chat experience.

Requirements

- Python 3.12+ (development and CI assume 3.12)
- The packages listed in `requirements.txt`.

Configuration (required environment variables)

- `GEMINI_API_KEY` — API key for Google Generative AI (used by `ChatGoogleGenerativeAI`).
- `NEWS_API_KEY` — API key for NewsAPI.org (used by `recent_news`).

Installation (local development)

1. Create a virtual environment and activate it:

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file (or export env vars) with the required API keys.

Running the application

```bash
streamlit run UI.py
```

The UI will be available at `http://localhost:8501` by default.

Docker

Build and run using the included `Dockerfile`:

```bash
docker build -t ai-agent .
docker run -p 8501:8501 --env-file .env ai-agent
```

Security notes

- Never commit `.env` or secrets. The provided `Dockerfile` copies `.env` during image build — avoid building images with secrets embedded. Use runtime secret injection in production.

Known limitations & recommended fixes

- `solve_math()` (in `main.py`) previously attempted to call `evalf()` on the raw result from `sympy.solve()`, which may return lists or symbolic objects; it has been updated to safely format numeric and symbolic solutions.
- `recent_news()` uses a fixed `from` date; make this parameter dynamic or controlled by user input.
- Several import paths (for `langchain` / `langgraph` / `google-genai` clients) may require version alignment with the `requirements.txt`. If import errors occur, consult the package docs or pin compatible versions.
- Network calls (news, model) lack robust timeout/retry/backoff strategies. Consider adding `timeout` parameters and improved exception handling.

Development & contribution

- Fork the repository and submit pull requests for fixes and features.
- Add unit tests for each tool (calculator, converter, math solver, news fetcher). A minimal CI workflow is recommended.

Troubleshooting

- If Streamlit fails to start, verify Python version and that dependencies are installed in the active environment.
- For API authentication issues, confirm that `GEMINI_API_KEY` and `NEWS_API_KEY` are set and valid.

License

Specify a license file or add an appropriate license section before publishing (MIT, Apache 2.0, etc.).

Contact

For questions or support, open an issue on the repository.
