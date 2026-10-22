```markdown
# Local Text-to-SQL Pipeline with LangChain & Ollama

An end-to-end Natural Language-to-SQL querying pipeline built with **LangChain (LCEL)**, **SQLite (Chinook database)**, and local inference powered by **Ollama (`llama3.2`)**. 

This system allows non-technical users to query relational databases using plain English without requiring manual SQL writing or cloud-based API calls.

---

## Architecture Overview

```text
User Question (Natural Language)
               │
               ▼
┌─────────────────────────────┐
│ 1. Schema Injection         │ ◄── Database DDL Schema (chinook.db)
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ 2. Text-to-SQL Generator    │ (Ollama llama3.2)
└──────────────┬──────────────┘
               ▼
         Raw SQL Query
               │
               ▼
┌─────────────────────────────┐
│ 3. Database Execution       │ ──► Runs on SQLite Engine
└──────────────┬──────────────┘
               ▼
       Raw Query Results
               │
               ▼
┌─────────────────────────────┐
│ 4. Natural Language Synth.  │ (Ollama llama3.2)
└──────────────┬──────────────┘
               ▼
Final Conversational Answer

```

---

## Features

* **100% Local Execution:** Uses local open-weights inference (`llama3.2`) via Ollama—no API keys, zero token fees, and complete data privacy.
* **Dynamic Schema Inspection:** Fetches live table names, column constraints, and foreign key definitions dynamically via LangChain's `SQLDatabase` wrapper.
* **Declarative LCEL Chains:** Built using LangChain Expression Language (`RunnablePassthrough`, `StrOutputParser`) for composability and predictable state routing.
* **Natural Language Synthesis:** Translates raw database tuples and records back into clean, user-friendly sentences.

---

## Project Structure

```text
.
├── chinook.db          # Sample SQLite database (digital media store)
├── texttosql.py        # Core pipeline execution script
├── requirements.txt    # Project Python dependencies
├── .env.example        # Environment configuration placeholder
└── README.md           # Documentation

```

---

## Prerequisites

1. **Python 3.10+** installed.
2. **Ollama** installed and running locally:
* Install from [ollama.com](https://ollama.com).
* Pull the required model:
```bash
ollama run llama3.2

```




3. **Chinook Database (`chinook.db`)**: Ensure the SQLite database file exists in the root directory.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone [https://github.com/](https://github.com/)<your-username>/<your-repo-name>.git
cd <your-repo-name>

```

### 2. Set Up a Virtual Environment

```bash
python -m venv .venv

# On Linux/macOS:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

*If creating `requirements.txt` manually, include:*

```text
langchain-core
langchain-community
langchain-ollama
python-dotenv

```

### 4. Run the Pipeline

```bash
python main.py

```

---

## Code Workflow Breakdown

1. **Database Connection (`Initialize Database`):**
Connects to `chinook.db` via `SQLDatabase.from_uri()` and defines helper functions to inspect schema DDL (`get_table_info()`) and execute queries (`run()`).
2. **SQL Generation (`Preparing Prompt`):**
Injects the database schema and user question into a strict system prompt instructing `llama3.2` to return only raw SQL statements.
3. **Query Execution & Synthesis (`answer_user_query`):**
* Chains the generated query into the database execution engine.
* Forwards the resulting record set and the original question to a second prompt for natural language conversion.



---

## Example Queries to Try

You can adjust the `query` variable in `main.py` to test different SQL complexities:

| Query Type | Example Question |
| --- | --- |
| **Simple Projection** | `"Give me the names of 10 Artists"` |
| **Multiple Columns** | `"Give me the name and artist ID of 10 Artists"` |
| **Foreign Key Filter** | `"Give me 10 Albums by the Artist with ID 1"` |
| **Table Join** | `"Give some Albums by the Artist name Audioslave"` |
| **Multi-Level Join** | `"Give some Tracks by the Artist name Audioslave"` |

---

## Recommended Improvements for Production

* **Read-Only Connections:** Connect via `sqlite:///chinook.db?mode=ro` to eliminate the risk of destructive operations (`DROP`, `DELETE`).
* **Markdown / Syntax Sanitization:** Add regex sanitizers to strip potential ````sql` code blocks produced by smaller LLMs.
* **Self-Correction / Retry Loop:** Wrap query execution in a `try/except` block to allow the LLM to fix syntax errors if SQLite execution fails.

```

<FollowUp>
Would you like me to add a troubleshooting section covering common Ollama connection issues and SQLite syntax cleanup tips to this README?
</FollowUp>

<ElicitationsGroup message="Next steps to expand your repository documentation:">
  <Elicitation label="Add a troubleshooting guide to the README" query="Provide a comprehensive troubleshooting section for this README covering Ollama port issues and SQLite parsing errors."/>
  <Elicitation label="Create a requirements.txt with pinned versions" query="Generate a complete requirements.txt with stable, pinned versions for langchain, langchain-ollama, and dependencies."/>
  <Elicitation label="Add sample command line interface (CLI) instructions" query="Show how to update main.py and this README to accept interactive user input from the terminal."/>
</ElicitationsGroup>

```
