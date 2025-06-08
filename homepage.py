import gc
import os
import pygame
import time
import serial
import customtkinter as ctk

from pyfirmata import Arduino, util

root = ctk.CTk()
root.title("Jogo da forca")
root.geometry("1000x600")
ctk.set_appearance_mode("System")

ARDUINO_PORT = "COM7"
conexao: None
# LED_PIN = 13
# ANALOG_PIN = 0


class ArduinoComunicator:

    # Método para inicializar tudo
    def __init__(self, port):
        self._port = port
        self._conexao = None
        self.Stabilize_Connection()

    def Stabilize_Connection(self):

        print(f"--Testando conexão com o {self._port}....--")
        try:
            self._conexao = serial.Serial(self._port, 9600, timeout=0.1)
            print(f"Conexão feita com sucesso na porta {self._port}!")
        except serial.SerialException as e:
            print(f"Algo deu muito errado {e}")
            self._conexao = None

    def Requisitar_Arduino_Dados(self, data):
        try:
            self._data = data + "\n"
            self._conexao.write(self._data.encode("utf-8"))
            print("Mensagem enviada.")
        except serial.SerialException as e:
            print(f"Algo deu muito errado: {e}")

    def Resposta_Arduino_Dados(self):
        try:
            self._data = self._conexao.readline().decode("utf-8").strip()
            print(f"Dados recebidos do arduino: {self._data}")
            return self._data

        except serial.SerialException as e:
            print(f"Erro ao receber os dados necessários: {e}")


# Válido lembrar que existe o "Master", que serve como "pano de fundo".
class GUI:
    # Método para incializar tudo.
    def __init__(self, master, arduino_port):
        self._master = master
        # Padrão decorator para usar outra classe e usa-la.
        self._initializer = ArduinoComunicator(arduino_port)

        # Primeiro frame
        self._frame1 = ctk.CTkFrame(master=self._master, height=600, width=1000)

        # Cabeçalho
        self._label1 = ctk.CTkLabel(
            master=self._frame1, text="Jogo da forca!", font=("Arial", 25, "bold")
        )
        # Outro cabeçalho
        self._label2 = ctk.CTkLabel(
            master=self._frame1,
            text="",
        )
        # Outro cabeçalho
        self._label_saida = ctk.CTkLabel(
            master=self._frame1, text="", font=("Roboto", 14, "italic")
        )

        self._input1 = ctk.CTkEntry(master=self._frame1, height=20, width=200)
        self._button_enter = ctk.CTkButton(
            master=self._frame1,
            width=200,
            height=20,
            text="Verficar",
            command=self.enviarDadoParaArduino,
        )

        self._frame1.pack(pady=20)
        self._label1.pack(pady=10)
        self._label2.pack(pady=10)
        self._input1.pack(pady=10)
        self._button_enter.pack(pady=10)
        self._label_saida.pack(pady=10)

    def enviarDadoParaArduino(self):
        message = self._input1.get()
        self._initializer.Requisitar_Arduino_Dados(message)
        self._label_saida.configure(text=message)
        self._suco = self._initializer.Resposta_Arduino_Dados()
        print("dados:" + self._suco)


if __name__ == "__main__":
    p = GUI(master=root, arduino_port=ARDUINO_PORT)
    root.mainloop()
