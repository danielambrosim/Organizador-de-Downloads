"""
Organizador de Downloads por Extensão
Move arquivos de uma pasta para subpastas baseado no tipo de arquivo.
"""

import argparse
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

# Mapeamento de extensões para pastas
EXTENSOES_PASTAS: Dict[str, str] = {
    # Imagens
    '.jpg': 'Imagens', '.jpeg': 'Imagens', '.png': 'Imagens', '.gif': 'Imagens',
    # PDFs
    '.pdf': 'PDFs',
    # Planilhas
    '.xls': 'Planilhas', '.xlsx': 'Planilhas', '.csv': 'Planilhas',
    # Documentos
    '.doc': 'Documentos', '.docx': 'Documentos', '.txt': 'Documentos',
    # Código
    '.py': 'Codigo', '.js': 'Codigo', '.html': 'Codigo', '.css': 'Codigo',
    # Áudio/Video
    '.mp3': 'Audio', '.mp4': 'Video',
    # Arquivos compactados
    '.zip': 'Compactados', '.rar': 'Compactados'
}

def obter_pasta_destino(arquivo: Path) -> str:
    """
    Determina a pasta destino baseado na extensão do arquivo.
    
    Args:
        arquivo: Caminho do arquivo
        
    Returns:
        Nome da pasta destino (ex: 'Imagens', 'PDFs')
    """
    extensao = arquivo.suffix.lower()
    return EXTENSOES_PASTAS.get(extensao, 'Outros')

def organizar_pasta(pasta: Path, dry_run: bool = False) -> Tuple[int, List[str]]:
    """
    Organiza os arquivos da pasta em subpastas por tipo.
    
    Args:
        pasta: Caminho da pasta a ser organizada
        dry_run: Se True, apenas simula sem mover arquivos
        
    Returns:
        Tupla (numero_movidos, lista_de_logs)
    """
    if not pasta.exists():
        raise FileNotFoundError(f"Pasta não encontrada: {pasta}")
    
    arquivos = [f for f in pasta.iterdir() if f.is_file()]
    movidos = 0
    logs = []
    
    for arquivo in arquivos:
        pasta_destino_nome = obter_pasta_destino(arquivo)
        pasta_destino = pasta / pasta_destino_nome
        
        if dry_run:
            log = f"[SIMULAÇÃO] {arquivo.name} -> {pasta_destino_nome}/"
            print(log)
            logs.append(log)
            movidos += 1
        else:
            # Cria a pasta destino se não existir
            pasta_destino.mkdir(exist_ok=True)
            
            destino = pasta_destino / arquivo.name
            shutil.move(str(arquivo), str(destino))
            log = f"[MOVIDO] {arquivo.name} -> {pasta_destino_nome}/"
            print(log)
            logs.append(log)
            movidos += 1
    
    return movidos, logs

def main():
    """Função principal com parsing de argumentos."""
    parser = argparse.ArgumentParser(
        description="Organiza arquivos por extensão em subpastas"
    )
    parser.add_argument(
        "--folder", 
        type=str, 
        default="./Downloads",  # Mude para "./pasta_simulada" no OnlineGDB
        help="Caminho da pasta a ser organizada"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula a organização sem mover arquivos"
    )
    
    args = parser.parse_args()
    pasta = Path(args.folder)
    
    print(f"📁 Organizando pasta: {pasta.absolute()}")
    print(f"🔍 Modo dry-run: {'SIM' if args.dry_run else 'NÃO'}")
    print("-" * 50)
    
    try:
        quantidade, _ = organizar_pasta(pasta, args.dry_run)
        print("-" * 50)
        print(f"✅ {quantidade} arquivos processados")
        
        if args.dry_run:
            print("💡 Execute sem --dry-run para realmente mover os arquivos")
            
    except Exception as erro:
        print(f"❌ Erro: {erro}")

if __name__ == "__main__":
    main()
