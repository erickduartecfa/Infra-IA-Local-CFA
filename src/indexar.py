import os
from pathlib import Path
import requests
from pypdf import PdfReader
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Configurações de Conexão Local (Loopback estrito)
QDRANT_HOST = os.getenv("QDRANT_HOST", "http://127.0.0.1:6333")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
COLLECTION_NAME = "cfa_conhecimento"

qdrant = QdrantClient(url=QDRANT_HOST)

def get_embedding(texto: str) -> list[float]:
    """Gera o vetor semântico (1024 dimensões) usando o modelo BGE-M3 no Ollama."""
    resp = requests.post(
        f"{OLLAMA_HOST}/api/embeddings",
        json={"model": "bge-m3", "prompt": texto},
        timeout=30
    )
    resp.raise_for_status()
    return resp.json()["embedding"]

def inicializar_colecao():
    """Recria a coleção no Qdrant com distância por cosseno e dimensão 1024."""
    qdrant.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
    )
    print(f"Coleção '{COLLECTION_NAME}' recriada com sucesso no Qdrant.")

def fatiar_texto(texto: str, tamanho_bloco: int = 400, sobreposicao: int = 60) -> list[str]:
    """Divide o texto em blocos de palavras com sobreposição para não perder contexto."""
    palavras = texto.split()
    blocos = []
    i = 0
    while i < len(palavras):
        bloco = " ".join(palavras[i:i + tamanho_bloco])
        blocos.append(bloco)
        i += max(1, tamanho_bloco - sobreposicao)
    return blocos

def indexar_arquivo_pdf(caminho_pdf: Path, titulo: str, link_origem: str = "https://cfa.org.br"):
    """Lê um PDF oficial do CFA, extrai texto, fatia em blocos e salva os embeddings no Qdrant."""
    if not caminho_pdf.exists():
        print(f"Arquivo não encontrado: {caminho_pdf}")
        return

    print(f"Lendo PDF: {titulo}...")
    reader = PdfReader(str(caminho_pdf))
    texto_total = ""
    for num, pag in enumerate(reader.pages):
        txt = pag.extract_text() or ""
        texto_total += f"\n[Página {num + 1}] " + txt

    blocos = fatiar_texto(texto_total)
    print(f"Gerando embeddings para {len(blocos)} trechos de '{titulo}'...")
    
    pontos = []
    for idx, bloco in enumerate(blocos):
        vetor = get_embedding(bloco)
        pontos.append(
            PointStruct(
                id=hash(f"{titulo}_{idx}") & 0x7FFFFFFF,
                vector=vetor,
                payload={
                    "documento": titulo,
                    "link_oficial": link_origem,
                    "trecho": bloco
                }
            )
        )
    
    qdrant.upsert(collection_name=COLLECTION_NAME, points=pontos)
    print(f"Sucesso: {len(pontos)} trechos salvos no Qdrant para o documento '{titulo}'.")

if __name__ == "__main__":
    inicializar_colecao()
    
    # Localiza o diretório data/raw_documents relativo à raiz do projeto
    raiz_projeto = Path(__file__).resolve().parent.parent
    pasta_docs = raiz_projeto / "data" / "raw_documents"
    
    arquivos = list(pasta_docs.glob("*.pdf"))
    if arquivos:
        for arq in arquivos:
            indexar_arquivo_pdf(arq, arq.name)
    else:
        print(f"Nenhum PDF encontrado em {pasta_docs}.")
        print("Insira os PDFs de normas do CFA nessa pasta e execute novamente.")
