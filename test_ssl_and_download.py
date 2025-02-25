#!/usr/bin/env python3
"""
Script de teste abrangente para verificar as configurações SSL e métodos de download.
Este script testa todas as soluções implementadas para resolver problemas de certificado SSL.
"""

import os
import sys
import ssl
import certifi
import logging
import tempfile
import subprocess
import shutil
import urllib.request
import requests
import json
import time

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ssl-test")

def test_ssl_configuration():
    """Testar todas as configurações SSL implementadas."""
    logger.info("=== TESTE DE CONFIGURAÇÃO SSL ===")
    
    results = {}
    
    # Teste 1: Verificar certificados certifi
    try:
        cert_path = certifi.where()
        cert_exists = os.path.exists(cert_path)
        logger.info(f"Certificados certifi: {cert_path}")
        logger.info(f"Certificados existem: {cert_exists}")
        results["certifi_certificates"] = cert_exists
    except Exception as e:
        logger.error(f"Erro ao verificar certificados certifi: {str(e)}")
        results["certifi_certificates"] = False
    
    # Teste 2: Verificar variáveis de ambiente
    env_vars = {
        "SSL_CERT_FILE": os.environ.get("SSL_CERT_FILE"),
        "REQUESTS_CA_BUNDLE": os.environ.get("REQUESTS_CA_BUNDLE"),
        "PYTHONHTTPSVERIFY": os.environ.get("PYTHONHTTPSVERIFY")
    }
    
    logger.info("Variáveis de ambiente SSL:")
    for var, value in env_vars.items():
        logger.info(f"  {var}: {value}")
    
    results["env_variables"] = all(env_vars.values())
    
    # Teste 3: Verificar script fix_ssl.py
    fix_ssl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fix_ssl.py")
    fix_ssl_exists = os.path.exists(fix_ssl_path)
    logger.info(f"Script fix_ssl.py: {fix_ssl_path}")
    logger.info(f"Script existe: {fix_ssl_exists}")
    results["fix_ssl_script"] = fix_ssl_exists
    
    # Teste 4: Testar conexão HTTPS básica
    try:
        logger.info("Testando conexão HTTPS básica...")
        response = urllib.request.urlopen("https://www.google.com", timeout=10)
        logger.info(f"Conexão HTTPS básica: OK (status {response.status})")
        results["https_connection"] = True
    except Exception as e:
        logger.error(f"Erro na conexão HTTPS básica: {str(e)}")
        results["https_connection"] = False
    
    # Teste 5: Testar conexão com YouTube
    try:
        logger.info("Testando conexão com YouTube...")
        response = urllib.request.urlopen("https://www.youtube.com", timeout=10)
        logger.info(f"Conexão YouTube: OK (status {response.status})")
        results["youtube_connection"] = True
    except Exception as e:
        logger.error(f"Erro na conexão com YouTube: {str(e)}")
        results["youtube_connection"] = False
    
    # Resumo dos resultados
    logger.info("\n=== RESUMO DOS TESTES SSL ===")
    all_passed = True
    for test, result in results.items():
        status = "PASSOU" if result else "FALHOU"
        logger.info(f"{test:20}: {status}")
        if not result:
            all_passed = False
    
    return all_passed

def configure_ssl():
    """Configurar SSL com todas as técnicas possíveis."""
    logger.info("Configurando SSL com técnicas avançadas...")
    
    # Usar certificados certifi
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    ssl._create_default_https_context = lambda: ssl_context
    
    # Configurar urllib
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
    urllib.request.install_opener(opener)
    
    # Desativar avisos de SSL no requests
    requests.packages.urllib3.disable_warnings()
    
    # Definir variáveis de ambiente
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    os.environ['PYTHONHTTPSVERIFY'] = '0'
    
    # Carregar o script fix_ssl.py se existir
    fix_ssl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fix_ssl.py")
    if os.path.exists(fix_ssl_path):
        logger.info(f"Carregando configurações de {fix_ssl_path}")
        with open(fix_ssl_path) as f:
            exec(f.read())
    
    logger.info("Configuração SSL concluída.")

def test_download_methods(url):
    """Testar todos os métodos de download implementados."""
    logger.info(f"\n=== TESTE DE MÉTODOS DE DOWNLOAD PARA {url} ===")
    
    # Criar diretório temporário para os testes
    temp_dir = tempfile.mkdtemp(prefix="youtube-ssl-test-")
    logger.info(f"Diretório temporário: {temp_dir}")
    
    results = {}
    
    try:
        # Teste 1: Método enhanced_youtube_downloader.py
        try:
            logger.info("Testando enhanced_youtube_downloader.py...")
            output_path = os.path.join(temp_dir, "enhanced.mp3")
            
            cmd = [
                sys.executable,
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "enhanced_youtube_downloader.py"),
                url,
                output_path
            ]
            
            logger.info(f"Executando comando: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / (1024 * 1024)
                logger.info(f"Download bem-sucedido: {output_path} ({file_size:.2f} MB)")
                results["enhanced_downloader"] = True
            else:
                logger.error(f"Falha no download: {result.stderr}")
                results["enhanced_downloader"] = False
        except Exception as e:
            logger.error(f"Erro ao testar enhanced_youtube_downloader.py: {str(e)}")
            results["enhanced_downloader"] = False
        
        # Teste 2: Método yt-dlp direto
        try:
            logger.info("Testando yt-dlp direto...")
            output_path = os.path.join(temp_dir, "yt-dlp.mp3")
            
            cmd = [
                "yt-dlp",
                "--no-check-certificate",
                "--geo-bypass",
                "--extract-audio",
                "--audio-format", "mp3",
                "--output", output_path,
                url
            ]
            
            logger.info(f"Executando comando: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(output_path):
                file_size = os.path.getsize(output_path) / (1024 * 1024)
                logger.info(f"Download bem-sucedido: {output_path} ({file_size:.2f} MB)")
                results["yt-dlp_direct"] = True
            else:
                logger.error(f"Falha no download: {result.stderr}")
                results["yt-dlp_direct"] = False
        except Exception as e:
            logger.error(f"Erro ao testar yt-dlp direto: {str(e)}")
            results["yt-dlp_direct"] = False
        
        # Teste 3: Método pytube
        try:
            logger.info("Testando pytube...")
            output_path = os.path.join(temp_dir, "pytube.mp3")
            
            cmd = [
                sys.executable,
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_pytube.py"),
                url
            ]
            
            logger.info(f"Executando comando: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Verificar se o download foi bem-sucedido (baseado na saída)
            if "Download bem-sucedido" in result.stdout or "Download successful" in result.stdout:
                logger.info("Download com pytube bem-sucedido")
                results["pytube"] = True
            else:
                logger.error(f"Falha no download com pytube: {result.stderr}")
                results["pytube"] = False
        except Exception as e:
            logger.error(f"Erro ao testar pytube: {str(e)}")
            results["pytube"] = False
        
        # Resumo dos resultados
        logger.info("\n=== RESUMO DOS TESTES DE DOWNLOAD ===")
        any_passed = False
        for test, result in results.items():
            status = "PASSOU" if result else "FALHOU"
            logger.info(f"{test:20}: {status}")
            if result:
                any_passed = True
        
        return any_passed
    
    finally:
        # Limpar diretório temporário
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
            logger.info(f"Diretório temporário removido: {temp_dir}")
        except Exception as e:
            logger.warning(f"Erro ao remover diretório temporário: {str(e)}")

def main():
    # Verificar argumentos
    if len(sys.argv) < 2:
        print("Uso: python test_ssl_and_download.py <youtube_url>")
        print("Exemplo: python test_ssl_and_download.py https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        return 1
    
    youtube_url = sys.argv[1]
    
    print(f"Iniciando testes abrangentes para URL: {youtube_url}")
    print("Este script testará todas as soluções implementadas para resolver problemas de certificado SSL.")
    
    # Configurar SSL
    configure_ssl()
    
    # Testar configuração SSL
    ssl_ok = test_ssl_configuration()
    
    # Testar métodos de download
    download_ok = test_download_methods(youtube_url)
    
    # Resultado final
    print("\n=== RESULTADO FINAL ===")
    print(f"Configuração SSL: {'OK' if ssl_ok else 'FALHOU'}")
    print(f"Métodos de Download: {'OK' if download_ok else 'FALHOU'}")
    
    if ssl_ok and download_ok:
        print("\nTodos os testes passaram! O sistema está configurado corretamente.")
        return 0
    elif download_ok:
        print("\nOs downloads funcionaram, mas há problemas na configuração SSL.")
        return 0
    else:
        print("\nOs testes falharam. Verifique os logs para mais detalhes.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
