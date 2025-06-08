import serial
import time
from pyfirmata import Arduino, util

ARDUINO_PORT = "COM7"
LED_PIN = 13
ANALOG_PIN = 0

print(f"--Testando conexão com o {ARDUINO_PORT}....--")

try:
    conexao = serial.Serial(ARDUINO_PORT, 9600, timeout=0.1)
    time.sleep(0.05)

    mensagem_para_enviar = "ligar led"
    mensagem_para_enviar_com_quebra = mensagem_para_enviar + "\n"
    pacote = mensagem_para_enviar_com_quebra.encode("utf-8")
    conexao.write(pacote)
    print(f"Mensagem enviada.")


except serial.SerialException as e:
    print(f"Algo deu muito errado {e}")

finally:
    if "conexao" in locals() and conexao.is_open:
        conexao.close()
        print("Conexão encerrada.")
