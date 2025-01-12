import speech_recognition as sr
import webbrowser

def ouvir_comando():

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ajustando para o ruído ambiente... Aguarde.")
        recognizer.adjust_for_ambient_noise(source)
        print("Pode falar agora...")
        try:
            audio = recognizer.listen(source, timeout=5)
            comando = recognizer.recognize_google(audio, language="pt-BR")
            print(f"Você disse: {comando}")
            return comando.lower()
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
 
    url = f"https://www.google.com/search?q={consulta.replace(' ', '+')}"
    webbrowser.open(url)
    print(f"Pesquisando: {consulta}")

def main():

    print("Bem-vindo ao assistente de pesquisa por voz!")
    while True:
        comando = ouvir_comando()
        if comando:
            if "pesquisar" in comando:
                consulta = comando.replace("pesquisar", "").strip()
                if consulta:
                    pesquisar_na_web(consulta)
                else:
                    print("Diga o que deseja pesquisar após 'pesquisar'.")
            elif comando in ["sair", "fechar", "parar"]:
                print("Encerrando o assistente. Até mais!")
                break
            else:
                print("Comando não reconhecido. Tente novamente.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAssistente encerrado pelo usuário.")
