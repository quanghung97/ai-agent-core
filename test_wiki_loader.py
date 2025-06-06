from langchain.document_loaders import WikipediaLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.vectorstores import Chroma
# from langchain.embeddings import OpenAIEmbeddings

# Bước 1: Lấy nội dung từ Wikipedia
loader = WikipediaLoader(query="Doraemon", lang="vi")  # hoặc lang="en"
docs = loader.load()
print(docs)


# Bước 2: Chia nhỏ
# splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# chunks = splitter.split_documents(docs)

# # Bước 3: Embedding và lưu vào Chroma
# embedding = OpenAIEmbeddings(model="text-embedding-ada-002")
# vectordb = Chroma.from_documents(chunks, embedding=embedding, persist_directory="chroma_doraemon/")
# vectordb.persist()
