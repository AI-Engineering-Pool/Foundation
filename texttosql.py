from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_ollama.llms import OllamaLLM


# 1. Initialize Database
db = SQLDatabase.from_uri("sqlite:///chinook.db", sample_rows_in_table_info=0)

def get_schema(_):
    return db.get_table_info()

def run_query(query):
    print("run_query Executed \n")
    print(f'Query being run >>> {query} \n')
    print("run_query Completed \n")
    return db.run(query)

print(get_schema(''))

print("Checkpoint-01 :: Initialize Database\n")

# 2. Preparing Prompt
def write_sql_query(llm):
    template = """Based on the table schema below, write a SQL query that would answer the user's question:
    {schema}
    Question: {question}
    SQL Query:"""

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Given an input question, convert it to a SQL query. No pre-amble. "
            "Please do not return anything else apart from the SQL query, no prefix aur suffix quotes, no sql keyword, nothing please"),
            ("human", template),
        ]
    )

    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()
    )

print("Checkpoint-02 :: Preparing Prompt\n")

def answer_user_query(query, llm):
    template = """Based on the table schema below, question, sql query, and sql response, write a natural language response:
    {schema}

    Question: {question}
    SQL Query: {query}
    SQL Response: {response}"""

    prompt_response = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Given an input question and SQL response, convert it to a natural language answer. No pre-amble.",
            ),
            ("human", template),
        ]
    )

    full_chain = (
        RunnablePassthrough.assign(query=write_sql_query(llm))
        | RunnablePassthrough.assign(
            schema=get_schema,
            response=lambda x: run_query(x["query"]),
        )
        | prompt_response
        | llm
    )

    return full_chain.invoke({"question": query})

# Query types to try out:

# 1. Straight forward queries: Give me the name of 10 Artists
# 2. Querying for multiple columns: Give me the name and artist ID of 10 Artists
# 3. Querying a table by a foreign key: Give me 10 Albums by the Artist with ID 1
# 4. Joining with a different table: Give some Albums by the Artist name Audioslave'
# 5. Multi-level Joins: Give some Tracks by the Artist name Audioslave'

load_dotenv()

# 3. Asking Human Query

query = 'Give some Albums by the Artist name Audioslave'

print("\nHuman Language Query >>> ",query, "\n")

print("Checkpoint-03 :: Translating and Executing Query\n")


# 4. Executting Query and Transfer the result set to Human Language
response = answer_user_query(query, llm = OllamaLLM(model="llama3.2"))

print("\n",response)

print("\nCheckpoint-04 :: All Process Completed\n")
