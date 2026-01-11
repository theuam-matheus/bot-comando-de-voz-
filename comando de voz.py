import speech_recognition as sr
from gtts import gTTS
import pygame
import io
import webbrowser
import os
import datetime
import time
import pyautogui
import tkinter as tk
from threading import Thread

# --- INTERFACE VISUAL ---
class InterfaceLuna:
    def __init__(self, root):
        self.root = root
        self.root.title("Luna - Assistente Virtual")
        self.root.geometry("400x420")
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#2c3e50")
        
        self.label_instrucao = tk.Label(root, text="COMO ME ATIVAR:\nDiga 'Luna' em voz alta", font=("Arial", 11, "bold"), fg="#3498db", bg="#2c3e50")
        self.label_instrucao.pack(pady=10)

        self.label_status = tk.Label(root, text="🔴 MODO DE ESPERA", font=("Arial", 14, "bold"), fg="#e74c3c", bg="#2c3e50")
        self.label_status.pack(pady=5)
        
        self.label_resposta = tk.Label(root, text="Luna: Aguardando chamado...", font=("Arial", 10, "italic"), 
                                       fg="#ecf0f1", bg="#34495e", wraplength=350, height=3)
        self.label_resposta.pack(pady=10, fill="x")
        
        tk.Label(root, text="COMANDOS DISPONÍVEIS:", font=("Arial", 10, "bold"), fg="#bdc3c7", bg="#2c3e50").pack()
        
        comandos_texto = ("• 'Abrir Youtube'\n"
                          "• 'Horas'\n"
                          "• 'Abrir Bloco de Notas'\n"
                          "• 'Pesquisar [termo]'\n"
                          "• 'Aumentar/Baixar Volume'\n"
                          "• 'Descansar'")
        
        self.txt_comandos = tk.Label(root, text=comandos_texto, font=("Arial", 10), 
                                     fg="#ecf0f1", bg="#2c3e50", justify="left")
        self.txt_comandos.pack(pady=5)

        self.label_dica = tk.Label(root, text="Dica: Após me ativar, não precisa repetir meu nome.", font=("Arial", 8), fg="#95a5a6", bg="#2c3e50")
        self.label_dica.pack(side="bottom", pady=10)

    def atualizar_status(self, ativo):
        if ativo:
            self.label_status.config(text="🟢 LUNA ATIVA", fg="#2ecc71")
            self.label_instrucao.config(text="ESTOU TE OUVINDO\nPode falar um comando", fg="#2ecc71")
        else:
            self.label_status.config(text="🔴 MODO DE ESPERA", fg="#e74c3c")
            self.label_instrucao.config(text="COMO ME ATIVAR:\nDiga 'Luna' em voz alta", fg="#3498db")

    def escrever_resposta(self, texto):
        self.label_resposta.config(text=f"Luna: {texto}")

# --- LÓGICA DA ASSISTENTE ---
class LunaInvisivel:
    def __init__(self, interface):
        self.interface = interface
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 100 
        self.recognizer.dynamic_energy_threshold = False 
        self.recognizer.pause_threshold = 0.6
        self.nome_ativacao = "luna"
        self.luna_acordada = False
        pygame.mixer.init()

    def falar(self, texto):
        print(f"Luna: {texto}")
        self.interface.escrever_resposta(texto)
        try:
            tts = gTTS(text=texto, lang='pt')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            pygame.mixer.music.load(fp)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        except Exception as e:
            print(f"Erro de áudio: {e}")

    def ouvir(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=5)
                return self.recognizer.recognize_google(audio, language="pt-BR").lower()
            except:
                return ""

    def executar_comando(self, comando):
        if not comando: return True

        if 'youtube' in comando:
            self.falar("Entendido. Abrindo o YouTube.")
            webbrowser.open("https://www.youtube.com")
        
        elif 'horas' in comando:
            hora = datetime.datetime.now().strftime('%H:%M')
            self.falar(f"Com certeza. Agora são {hora}.")
        
        elif 'bloco de notas' in comando:
            self.falar("Certo. Abrindo o bloco de notas.")
            os.system("notepad")

        elif 'pesquisar' in comando:
            termo = comando.replace('pesquisar', '').strip()
            self.falar(f"Vou pesquisar {termo} no Google.")
            webbrowser.open(f"https://www.google.com/search?q={termo}")

        elif 'volume' in comando:
            if 'aumentar' in comando:
                self.falar("Aumentando o volume.")
                for _ in range(5): pyautogui.press("volumeup")
            else:
                self.falar("Baixando o volume.")
                for _ in range(5): pyautogui.press("volumedown")

        elif 'descansar' in comando or 'dormir' in comando:
            self.falar("Modo de espera ativado. Me chame pelo nome.")
            self.luna_acordada = False
            self.interface.atualizar_status(False)
            return True

        elif any(p in comando for p in ['sair', 'desligar']):
            self.falar("Desligando. Até mais!")
            self.interface.root.quit()
            return False
        
        return True

    def loop_principal(self):
        self.falar("Luna pronta.")
        while True:
            frase = self.ouvir()
            if not self.luna_acordada:
                if self.nome_ativacao in frase:
                    self.luna_acordada = True
                    self.interface.atualizar_status(True)
                    self.falar("Sim, pode falar. Meus comandos estão na sua tela.")
            else:
                if frase:
                    if not self.executar_comando(frase):
                        break
            time.sleep(0.1)

# --- EXECUÇÃO ---
if __name__ == "__main__":
    root = tk.Tk()
    app_ui = InterfaceLuna(root)
    assistente = LunaInvisivel(app_ui)
    thread_luna = Thread(target=assistente.loop_principal, daemon=True)
    thread_luna.start()
    root.mainloop()