#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import chromadb
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.agents.agent_toolkits import create_retriever_tool

from langchain.text_splitter import CharacterTextSplitter

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.messages import SystemMessage
from langchain_openai import OpenAIEmbeddings, ChatOpenAI


async def run_agent(user_input: str, system_prompt: str) -> str:
    persist_directory = './tmp/state_of_union_db'
    client = chromadb.PersistentClient(path=persist_directory)

    embeddings = OpenAIEmbeddings()

    if client.count_collections() == 0:
        # Load the document, split it into chunks, embed each chunk and load it into the vector store.
        raw_documents = TextLoader('./resources/state_of_the_union.txt', "utf-8").load()
        text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=0)
        documents = text_splitter.split_documents(raw_documents)
        # 新しいDBの作成
        db = Chroma(
            collection_name="state_of_union_store",
            embedding_function=embeddings,
            client=client,
        )
        db.add_documents(documents=documents, embedding=embeddings)
    else:
        db = Chroma(
            collection_name="state_of_union_store",
            embedding_function=embeddings,
            client=client,
        )

    retriever = db.as_retriever()
    tool = create_retriever_tool(
        retriever,
        "search_state_of_union",
        "一般教書に関する文書を検索して返却します。",
    )
    tools = [tool]
    llm = ChatOpenAI(model='gpt-3.5-turbo-0125', temperature=0)
    prompt = hub.pull('hwchase17/openai-tools-agent')
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    result = await agent_executor.ainvoke({
        'chat_history': [
            SystemMessage(content=system_prompt),
        ],
        'input': user_input
    })
    print(result['output'])
    return result['output']
