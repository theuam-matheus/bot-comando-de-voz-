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
        self.root.title("Luna Status")
        self.root.geometry("300x150")
        self.root.attributes("-topmost", True)
        
        self.label = tk.Label(root, text="🔴 Modo de Espera", font=("Arial", 14, "bold"), fg="red")
        self.label.pack(expand=True)
        
        self.sub_label = tk.Label(root, text="Diga 'Luna' para ativar", font=("Arial", 10), fg="gray")
        self.sub_label.pack(pady=10)

    def atualizar_status(self, ativo):
        if ativo:
            self.label.config(text="🟢 LUNA ATIVA", fg="green")
            self.sub_label.config(text="Ouvindo comandos...")
        else:
            self.label.config(text="🔴 Modo de Espera", fg="red")
            self.sub_label.config(text="Diga 'Luna' para ativar")

# --- LÓGICA DA ASSISTENTE ---
class LunaInvisivel:
    def __init__(self, interface):
        self.interface = interface
        self.recognizer = sr.Recognizer()
        
        # --- AJUSTES DE SENSIBILIDADE ---
        self.recognizer.energy_threshold = 1g
        self.nome_ativacao = "luna"
        self.luna_acordada = False
        pygame.mixer.init()

    def falar(self, texto):
        print(f"Luna: {texto}")
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
            # Calibração mais curta para não "surdar" a assistente
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                print(">>> Escutando (Alta Sensibilidade)...")
                # phrase_time_limit curto ajuda a processar o nome rápido
                audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=4)
                texto = self.recognizer.recognize_google(audio, language="pt-BR").lower()
                print(f"Você disse: {texto}")
                return texto
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
            self.falar("Modo de espera ativado. Me chame pelo nome se precisar.")
            self.luna_acordada = False
            self.interface.atualizar_status(False)
            return True

        elif any(p in comando for p in ['sair', 'desligar']):
            self.falar("Desligando assistente. Até logo!")
            self.interface.root.quit()
            return False
        
        return True

    def loop_principal(self):
        self.falar("Luna iniciada. Estou ouvindo.")
        
        while True:
            frase = self.ouvir()
            
            if not self.luna_acordada:
                # O uso de 'in' permite que ela entenda se você disser "Luna, está aí?"
                if self.nome_ativacao in frase:
                    self.luna_acordada = True
                    self.interface.atualizar_status(True)
                    self.falar("Sim, pode falar. Meus comandos são: YouTube, Horas, Bloco de notas, Pesquisar, Volume e Descansar.")
            else:
                if frase:
                    if not self.executar_comando(frase):
                        break
            time.sleep(0.1)

if __name__ == "__main__":
    root = tk.Tk()
    app_ui = InterfaceLuna(root)
    assistente = LunaInvisivel(app_ui)
    
    thread_luna = Thread(target=assistente.loop_principal, daemon=True)
    thread_luna.start()
    
    root.mainloop()