#  Copyright (c) 2024 LongbowXXX
#
#  This software is released under the MIT License.
#  http://opensource.org/licenses/mit-license.php
import chromadb
from langchain.agents.agent_toolkits import create_conversational_retrieval_agent
from langchain.agents.agent_toolkits import create_retriever_tool

from langchain.text_splitter import CharacterTextSplitter

from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI


async def run_agent() -> str:
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
    llm = ChatOpenAI(temperature=0)
    agent_executor = create_conversational_retrieval_agent(llm, tools, verbose=True)
    result = await agent_executor.ainvoke({
        "input": "大統領は最新の一般教書でケタンジ・ブラウン・ジャクソンについて何と言いましたか?簡潔に答えてください。"
    })
    # result = agent_executor(
    #     {
    #         "input": "大統領は最新の一般教書でケタンジ・ブラウン・ジャクソンについて何と言いましたか?簡潔に答えてください。"
    #     }
    # )
    print(result["output"])
    return result["output"]
