import speech_recognition as sr
import webbrowser
from urllib.parse import quote_plus
import time
import sys

def ouvir_comando(timeout_listen=5, timeout_phrase=2, ajuste_ruido=1):
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\nAjustando para o ruído ambiente... Aguarde.")
        recognizer.adjust_for_ambient_noise(source, duration=ajuste_ruido)
        print("Pode falar agora...")
        
        try:
            audio = recognizer.listen(source, timeout=timeout_listen, phrase_time_limit=timeout_phrase)
            comando = recognizer.recognize_google(audio, language="pt-BR")
            print(f"Você disse: {comando}")
            return comando.lower()
        except sr.WaitTimeoutError:
            print("Tempo de espera esgotado. Por favor, tente novamente.")
            return None
        except sr.UnknownValueError:
            print("Não entendi o que você disse. Tente novamente.")
            return None
        except sr.RequestError as e:
            print(f"Erro ao acessar o serviço de reconhecimento de fala: {e}")
            return None
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return None

def pesquisar_na_web(consulta):
    if not consulta or consulta.isspace():
        print("Consulta de pesquisa vazia.")
        return
    
    query_segura = quote_plus(consulta)
    url = f"https://www.google.com/search?q={query_segura}"
    webbrowser.open(url)
    print(f"Pesquisando: {consulta}")

def abrir_site(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        webbrowser.open(url)
        print(f"Abrindo: {url}")
    except Exception as e:
        print(f"Erro ao tentar abrir o site: {e}")

def processar_comando(comando):
    if not comando:
        return True
    
    comandos = {
        'pesquisar': lambda c: pesquisar_na_web(c.replace('pesquisar', '').strip()),
        'abrir': lambda c: abrir_site(c.replace('abrir', '').strip()),
        'sair': lambda _: False,
        'fechar': lambda _: False,
        'parar': lambda _: False,
        'encerrar': lambda _: False
    }
    
    for palavra_chave, acao in comandos.items():
        if palavra_chave in comando:
            return acao(comando)
    
    print("Comando não reconhecido. Comandos disponíveis:")
    print("- Pesquisar [termo]")
    print("- Abrir [site]")
    print("- Sair / Fechar / Parar / Encerrar")
    return True

def mostrar_ajuda():
    print("\nComandos disponíveis:")
    print("- 'Pesquisar [termo]' - Faz uma pesquisa no Google")
    print("- 'Abrir [site]' - Abre um site (ex: 'abrir youtube.com')")
    print("- 'Sair', 'Fechar', 'Parar' ou 'Encerrar' - Finaliza o programa")
    print("\nAguarde o aviso 'Pode falar agora...' antes de ditar seu comando.")

def verificar_microfone():
    try:
        with sr.Microphone() as source:
            pass
        return True
    except OSError:
        print("Microfone não encontrado. Conecte um microfone e tente novamente.")
        return False

def main():
    print("=== Assistente de Pesquisa por Voz ===")
    mostrar_ajuda()
    
    if not verificar_microfone():
        sys.exit(1)
    
    try:
        while True:
            comando = ouvir_comando()
            if not processar_comando(comando):
                print("Encerrando o assistente. Até mais!")
                break
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nAssistente encerrado pelo usuário.")
    except Exception as e:
        print(f"\nErro crítico: {e}")
        print("O assistente será encerrado.")

if __name__ == "__main__":
    main()
