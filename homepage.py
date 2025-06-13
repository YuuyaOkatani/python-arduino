import gc
import os
import pygame
import time
import serial
import customtkinter as ctk
import threading
import ast
from PIL import Image, ImageTk

root = ctk.CTk()
image = Image.open("images/festa_junina_com_fundo_laranja_2.png    ")
background_image = ctk.CTkImage(image, size=(1000, 600))
root.title("Jogo da forca")
root.geometry("1000x600")
ctk.set_appearance_mode("System")


ARDUINO_PORT = "COM6"
conexao = None


class ArduinoComunicator:

    # Método para inicializar tudo (Válido lembrar que "self" serve para criar qualquer variável.)
    def __init__(self, port):
        self._port = port
        self._conexao = None
        self._is_reading_true = True
        self._quantidade_vidas = 6
        self._erros = 0
        self._dica = ""
        self._segredo = ""
        self._letra_ja_digitada = False
        self._is_game_over = False
        self._is_level_complete = False
        self._is_caracter_valid_false = False

        self.Stabilize_Connection()

    # Método para realizar uma conexão com a porta de arduino.
    def Stabilize_Connection(self):

        print(f"--Testando conexão com o {self._port}....--")
        try:
            self._conexao = serial.Serial(self._port, 9600, timeout=0.1)
            time.sleep(2)
            self._conexao.reset_input_buffer()
            print(f"Conexão feita com sucesso na porta {self._port}!")
            read_thread = threading.Thread(
                target=self.Receber_dados_continuamente, daemon=True
            )
            read_thread.start()

        except serial.SerialException as e:
            print(f"Algo deu muito errado {e}")
            self._conexao = None

    # Realiza conexão com threading para não consumir totalmente a memória.
    def Receber_dados_continuamente(self):
        while self._is_reading_true:
            try:
                if self._conexao and self._conexao.in_waiting > 0:
                    received_data = self._conexao.readline().decode("utf-8").strip()
                    self._is_game_over = False
                    self._is_level_complete = False
                    # Condições necessárias para interpretar os dados do arduino.
                    # Aqui pode realizar mudanças de variáveis para qualquer
                    # palavra-chave que seu ARDUINO através da outra porta.

                    # Ex: se tiver palavra "dica" no Serial.println("dica"),
                    # então vai acionar o que está dentro da condição.
                    if "dica" in received_data.lower().strip():
                        print(f"Dica: { received_data}")
                        self._dica = received_data

                        time.sleep(0.01)

                    if "segredo" in received_data.lower().strip():
                        print(f"palavra sorteada: {received_data}")
                        self._segredo = (
                            received_data.strip().replace("segredo:", "").strip()
                        )

                        print(f"Dados formatados do segredo: {self._segredo}")

                        time.sleep(0.01)

                    if "erros" in received_data.lower().strip():
                        print(f"Quantidade de erros {received_data}")
                        self._erros = int(
                            received_data.strip().replace("erros:", "").strip()
                        )
                        print(f"Dados formatados erros: {self._erros}")
                        time.sleep(0.01)
                    if "vidas" in received_data.lower().strip():
                        print(f"Quantidade de vidas: {received_data}")
                        self._quantidade_vidas = int(
                            received_data.strip().replace("vidas:", "").strip()
                        )
                        print(f"Dados formatados vidas: {self._quantidade_vidas}")
                        time.sleep(0.01)
                    if "letra_ja_selecionada" in received_data.lower().strip():
                        print(f"Letra já selecionada. Digite outro. {received_data}")
                        self._letra_ja_digitada = True
                        time.sleep(0.01)

                    if "gameover" in received_data.lower().strip():
                        print(f"GAME OVER")
                        self._is_game_over = True

                    if "levelcomplete" in received_data.lower().strip():
                        print(f"LEVEL COMPLETE")
                        self._is_level_complete = True

                    if "digiteumcaraterevalido" in received_data.lower().strip():
                        print("Digite um caractere válido")
                        self._is_caracter_valid_false = True

                    if "resetgame" in received_data.lower().strip():

                        print("Jogo resetado.")

                    print("Dados do arduino: " + received_data.lower().strip())

                    time.sleep(0.02)

            except serial.SerialException as e:
                print(f"Algo deu errado no recebimento contínuo de dados: {e}")
                self._is_reading_true = False
                if self._conexao:
                    self._conexao.close()
                self._conexao = None
                print("Conexão foi desligada por causa de um erro.")
                break
            except Exception as e:
                print(f"Algo deu errado no recebimento contínuo de dados: {e}")
                self._is_reading_true = False
                break

    # Método que enviar dados para outra porta do par COM
    def Requisitar_Arduino_Dados(self, data):
        try:
            self._data = data + "\n"
            self._conexao.write(self._data.encode("utf-8"))
            print("Mensagem enviada.")
            self._letra_ja_digitada = False
            self._is_caracter_valid_false = False
            self._is_game_over = False
            self._is_level_complete = False
        except serial.SerialException as e:
            print(f"Algo deu muito errado: {e}")

    # Envia os estados modificados pela resposta das condições do arduino.
    def Reposta_arduino_dados(self):
        return (
            self._quantidade_vidas,
            self._erros,
            self._dica,
            self._segredo,
            self._letra_ja_digitada,
            self._is_game_over,
            self._is_level_complete,
            self._is_caracter_valid_false,
        )


# Válido lembrar que existe o "Master", que serve como "pano de fundo".
class GUI:
    # Método para incializar tudo.
    def __init__(self, master, arduino_port):
        self._master = master
        # Padrão decorator para usar outra classe e usa-la.
        self._initializer = ArduinoComunicator(arduino_port)
        self._escutando = False
        # Primeiro frame
        self._frame1 = ctk.CTkFrame(master=self._master, height=800, width=1000)
        self._label_image = ctk.CTkLabel(
            self._frame1, image=background_image, text=None
        )
        self._vidas = 6
        self._erros = 0
        self._dicas = ""
        self._segredo = ""

        # Define a image de fundo.

        # Cabeçalho
        self._label1 = ctk.CTkLabel(
            master=self._frame1,
            text="Jogo da forca!",
            font=("Arial", 25, "bold"),
            fg_color="#FF7A00",
            bg_color="#FF7A00",
        )

        # Outro cabeçalho
        self._label2 = ctk.CTkLabel(
            master=self._frame1,
            text="",
            font=("Arial", 25, "bold"),
            fg_color="#FF7A00",
            bg_color="#FF7A00",
        )

        self._label3 = ctk.CTkLabel(
            master=self._frame1,
            text=None,
            font=("Arial", 25, "bold"),
            fg_color="#FF7A00",
            bg_color="#FF7A00",
        )
        self._label4 = ctk.CTkLabel(
            master=self._frame1,
            text=None,
            font=("Arial", 25, "bold"),
            fg_color="#FF7A00",
            bg_color="#FF7A00",
        )
        self._label5 = ctk.CTkLabel(
            master=self._frame1,
            text=None,
            font=("Arial", 25, "bold"),
            fg_color="#FF7A00",
            bg_color="#FF7A00",
        )

        # Outro cabeçalho
        self._label_saida = ctk.CTkLabel(
            master=self._frame1,
            text="",
            font=("Arial", 25, "bold"),
            fg_color="#FF7A00",
            bg_color="#FF7A00",
        )

        self._input1 = ctk.CTkEntry(master=self._frame1, height=20, width=200)
        self._button_enter = ctk.CTkButton(
            master=self._frame1,
            width=200,
            height=50,
            bg_color="#34eb58",
            text="Verficar",
            command=self.enviarDadoParaArduino,
        )

        # Para enpacotar tudo e mostrar na interface.
        self._label_image.place(x=0, y=0)
        self._frame1.pack(pady=50, fill="both", expand=True)

        self._label1.pack(pady=10)
        self._label2.pack(pady=10)
        self._label3.pack(pady=10)
        self._input1.pack(pady=10)
        self._label4.pack(pady=10)
        self._label5.pack(pady=10)
        self._button_enter.pack(pady=10)
        self._label_saida.pack(pady=10)

        root.bind("<Configure>", self.bg_resizer)

    # Enviar e receber os dados do arduino.
    def enviarDadoParaArduino(self):
        message = self._input1.get()
        if message.isalpha():
            if len(message.lower().strip()) > 1 or len(message.lower().strip()) < 1:
                self._label_saida.configure(text="Digite apenas um caractere :)")
            else:
                self._initializer.Requisitar_Arduino_Dados(message)
                self._label_saida.configure(text=f"letra digitada: {message}")

        else:
            self._label_saida.configure(text="Selecione caractere válido :)")

    def bg_resizer(self, e):
        if e.widget is root:
            i = ctk.CTkImage(image, size=(e.width, e.height))
            self._label_image.configure(text="", image=i)

    # Método para conseguir resposta do arduino de forma cotínua, atualizando a cada segundo.
    def escutar_dados_connector_arduino(self):
        while self._escutando:
            (
                self._vidas,
                self._erros,
                self._dicas,
                self._segredo,
                self._letra_ja_selecionada,
                self._is_game_over,
                self._is_level_complete,
                self._is_caractere_valid_false,
            ) = self._initializer.Reposta_arduino_dados()

            self._label2.configure(text=self._dicas)
            self._label3.configure(text=" ".join(self._segredo))
            self._label4.configure(text=f"Vidas: {self._vidas}")
            self._label5.configure(text=f"Erros: {self._erros}")
            if self._letra_ja_selecionada == True:
                self._label_saida.configure(text="Letra já selecionada. Escolha outro.")

            if self._is_game_over == True:
                self._label_saida.configure(text="GAME OVER")
                time.sleep(8)
                self._label_saida.configure(text="")

            if self._is_level_complete == True:
                self._label_saida.configure(text="você venceu!")
                time.sleep(8)
                self._label_saida.configure(text="")

            if self._is_caractere_valid_false == True:
                self._label_saida.configure(text="Selecione caractere válido")

            time.sleep(0.5)

    # Método para executar a escuta através da Multithreading.
    def executar_escuta(self):
        self._escutando = True
        self._thread = threading.Thread(
            target=self.escutar_dados_connector_arduino, daemon=True
        )
        self._thread.start()
        print("Escuta em segundo plano realizado com sucesso.")

    # Desligar a escuta.
    def parar_escuta(self):
        self._escutando = False
        self._thread.join()
        print("Escuta desligada com sucesso.")


if __name__ == "__main__":
    p = GUI(master=root, arduino_port=ARDUINO_PORT)
    p.executar_escuta()

    root.mainloop()
