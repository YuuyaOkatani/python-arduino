import serial
import time
import threading
import pygame

VIRTUAL_ARDUINO_PORT = "COM6"
BAUD_RATE = 9600

PALAVRAS = [
    "FORRO",
    "FOGOS",
    "QUENTAO",
    "BARRACA",
    "PACOCA",
    "TRILHA",
    "QUERMESSE",
    "BALÃO",
    "FITA",
    "COCADA",
    "MANJERICAO",
    "ARRAIAL",
    "PIPOCA",
    "CAPIVARA",
    "GAMBA",
    "ANTA",
    "TUCANO",
    "LEMURE",
    "EMA",
    "JAVALI",
    "MICO-LEAO",
    "CORVO",
    "AXOLOTE",
    "CORUJA",
    "LONTRA",
    "TESOURA",
    "LANTERNA",
    "ESPELHO",
    "RELOGIO",
    "FONES",
    "JANELA",
    "TRAVESSEIRO",
    "TECLADO",
    "ESCADA",
    "BUSSOLA",
    "COFRE",
    "GUARDA-CHUVA",
    "MORSE",
    "EGITO",
    "SERTAO",
    "LABIRINTO",
    "CANADA",
    "ESTUFA",
    "GRECIA",
    "MARROCOS",
    "OBSERVATORIO",
    "FAROL",
    "ILHAS MALDIVAS",
    "DESFILADEIRO",
    "TOQUIO",
]
DICAS = [
    "Estilo musical dançado colado, típico do Nordeste.",
    "Estalam no céu durante a comemoração.",
    "Bebida quente com gengibre e especiarias.",
    "Estrutura onde ocorrem jogos e vendas.",
    "Doce feito de amendoim e muito presente na festa.",
    "Caminho estreito, geralmente em meio a natureza, feito a pé",
    "Evento popular com barracas, comidas típicas e sorteios.",
    "Sobe aos céus colorido, mas hoje é proibido.",
    "Usada para enfeitar trajes e cabelos.",
    "Doce de coco feito em casa.",
    "Planta aromática usada em simpatias de Santo Antônio.",
    "Espaço onde ocorre a festa popular.",
    "Explode ao aquecer, muda de forma e sabor",
    "Maior roedor do mundo, vive em bandos.",
    "Se defende com um odor inconfundível.",
    "Mamífero grande e tímido da fauna brasileira.",
    "Ave tropical de bico grande e colorido, comum em florestas brasileiras.",
    "Primata noturno de olhos grandes, nativo de Madagascar.",
    "Ave corredora, grande e sem asas, típica do cerrado.",
    "Porco selvagem com presas, encontrado em florestas e campos.",
    "Pequeno primata dourado em risco de extinção.",
    "Ave associada a mistério e inteligência.",
    "Anfíbio mexicano que nunca completa a metamorfose.",
    "Ave noturna com visão apurada e símbolo de sabedoria.",
    "Mamífero ágil que nada muito bem e costuma brincar com pedras no rio.",
    "Serve para cortar papel ou tecido.",
    "Ilumina em lugares escuros.",
    "Reflete sua imagem de volta.",
    "Marca o tempo e fica no pulso.",
    "Usado para ouvir música sem incomodar.",
    "Deixa o vento e a luz entrarem.",
    "Apoia a cabeça para dormir.",
    "Digitador indispensável no computador.",
    "Ajuda a alcançar lugares altos.",
    "Aponta sempre para o norte.",
    "Guarda coisas de valor.",
    "Protege da chuva repentina.",
    "Código que transmite letras com pontos e traços.",
    "País africano famoso por suas pirâmides.",
    "Região marcada pela seca e resistência.",
    "Lugar onde se entra sem saber como sair.",
    "Segundo maior país do mundo, conhecido por florestas, lagos e frio intenso.",
    "Ambiente fechado que controla o espaço interno para cultivar ou fazer experimentos",
    "Berço da filosofia ocidental e dos Jogos Olímpicos antigos.",
    "País do norte da África com cultura árabe e mercados coloridos.",
    "Lugar de estudo das estrelas.",
    "Guia marítimo nas noites escuras.",
    "Arquipélago tropical asiático famoso por suas águas cristalinas e resorts flutuantes.",
    "Vale profundo entre grandes rochas.",
    "Megacidade asiática onde a tecnologia encontra tradições milenares.",
]
print(f"Iniciando conexão na porta {VIRTUAL_ARDUINO_PORT}...")


try:
    ser = serial.Serial(VIRTUAL_ARDUINO_PORT, BAUD_RATE, timeout=0.1)
    time.sleep(1)
    print(f"Conexão bem-sucedida na porta {VIRTUAL_ARDUINO_PORT}!")

    while True:
        if ser.in_waiting > 0:
            received_data = ser.readline().decode("utf-8").strip()
            print(f"[RX] Recebido do Comptador: {received_data}")

            if received_data.strip() == "":
                response = "Digite algo!"
            else:
                response = "Dados recebidos: " + received_data
            ser.write(response.encode("utf-8"))
            print(f"[TX] Enviado ao PC: {response.strip()}")
        time.sleep(0.05)

except serial.SerialException as e:
    print(f"Algo de errado na porta emulador: {e}")

except KeyboardInterrupt:
    print("Simulador encerrado")
finally:
    if "ser" in locals() and ser.is_open:
        ser.close()
        print("Porta do simulador fechado")
