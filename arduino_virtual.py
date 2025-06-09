import serial
import time
import threading
import pygame
import random

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


class ArduinoVirtual:
    def __init__(self, port, baudrate):
        self._vidas = 6
        self._erros = 0
        self._port = port
        self._baudrate = baudrate

        # Pega um número aleatório.
        self._numero_aleatorio = random.randint(1, 50)

        # Cria uma variável e seleciona uma palavra aleatória através de um index.
        self._mensagem_segredo_real = PALAVRAS[self._numero_aleatorio]

        # Mascara a palavra aleatóriamente selecionada.
        self._dados_segredo = self.mascarar_palavra(self._mensagem_segredo_real)

        # Para verificar se houve alguma mudança na palavra secreta.
        self._chance_mudanca = False

        # Iniciar arduino quando a classe for instanciada.
        self.Iniciar_arduino()

    def mascarar_palavra(self, mensagem):
        palavra_mascarada = []
        for letra in mensagem:
            if letra.isalpha():
                palavra_mascarada.append("_")
            elif letra == " ":
                palavra_mascarada.append(" ")
            elif letra == "-":
                palavra_mascarada.append("-")
        return "".join(palavra_mascarada)

    # método que vai adicionar as letras. (palavra já modificada, palavra selecionada da lista letra selecionada)
    def adicionar_palavra(self, letra_selecionada):
        palavra_mascarada = []

        # Para cada letra da palavra já modificada,
        # com letras, se tiver uma letra semelhante a selecionada,
        # não será adicionada novamente.

        # Para cada letra da palavra que foi selecionado no sorteio, é inserido nova letra.
        # Ex:
        # Palavra: ARRAIA
        # palavra já modificada: _RR_I_
        for i in range(len(self._mensagem_segredo_real)):
            if self._dados_segredo[i].isalpha():
                palavra_mascarada.append(self._dados_segredo[i])
            elif self._dados_segredo[i] == "-":
                palavra_mascarada.append("-")
            elif self._mensagem_segredo_real[i] == letra_selecionada:
                palavra_mascarada.append(self._mensagem_segredo_real[i])
            else:
                palavra_mascarada.append("_")

        return "".join(palavra_mascarada)

    def Iniciar_arduino(self):
        # Para acionar o pySerial. Enquanto for verdadeiro, o pySerial contiunará funcionando.
        self._on_active = True
        try:
            ser = serial.Serial(self._port, self._baudrate, timeout=0.1)
            time.sleep(1)
            print(f"Conexão bem-sucedida na porta {self._port}!")

            pygame.init()
            pygame.mixer.init()

            # Colocando uma variável para verificar se há diferença entre a palavra anterior e o atual
            # Ex: __ATO == ____ (prato)?

            mensagem_dica_teste = "Dica: " + DICAS[self._numero_aleatorio] + "\n"

            mensagem_dados_segredo = "Segredo: " + self._dados_segredo + "\n"
            mensagem_vidas = "Vidas: " + str(self._vidas) + "\n"

            mensagem_erros = f"Erros: {str(self._erros)}" + "\n"

            message_reset = "resetgame" + "\n"
            ser.write(mensagem_dica_teste.encode("utf-8"))
            ser.write(mensagem_dados_segredo.encode("utf-8"))
            ser.write(mensagem_vidas.encode("utf-8"))
            ser.write(mensagem_erros.encode("utf-8"))

            ser.write(message_reset.encode("utf-8"))
            while self._on_active:

                if ser.in_waiting > 0:
                    received_data = ser.readline().decode("utf-8").strip()
                    print(f"[RX] Recebido do Comptador: {received_data}")

                    if (
                        len(received_data.strip()) > 1
                        or len(received_data.strip()) < 1
                        or not received_data.strip().isalpha()
                    ):
                        print("Digite um caractere válido")
                        self._chance_mudanca = True
                        mensagem_digite_um_caractere_valido = (
                            "digiteumcaraterevalido" + "\n"
                        )
                        ser.write(mensagem_digite_um_caractere_valido.encode("utf-8"))
                    # Para cada letra da palavra real, verfica se a letra existe
                    elif len(received_data.strip()) == 1:
                        if received_data.strip().upper() in self._dados_segredo:
                            print("Letra já selecionada. Selecione outros.")
                            mensagem_letra_ja_selecionada = (
                                "Letra_ja_selecionada:"
                                + received_data.strip().upper()
                                + "\n"
                            )
                            ser.write(mensagem_letra_ja_selecionada.encode("utf-8"))
                            self._chance_mudanca = True
                        else:
                            for letter in self._mensagem_segredo_real:
                                if letter == received_data.upper().strip():
                                    # Modifica a palavra caso letra exista
                                    self._dados_segredo = self.adicionar_palavra(letter)
                                    self._chance_mudanca = True
                                # Verifica se houve alguma mudança na palavra.
                    if self._chance_mudanca == False:
                        self._vidas -= 1
                        self._erros += 1

                        self._chance_mudanca = False
                    else:
                        self._chance_mudanca = False
                    # Envia todos os dados para serem filtrados pelo programa python
                    mensagem_vidas = f"Vidas: {str(self._vidas)}" + "\n"
                    mensagm_erros = "Erros: " + str(self._erros) + "\n"
                    mensagem_dados_segredo = "Segredo: " + self._dados_segredo + "\n"

                    print(f"Quantidade de vidas: {str(self._vidas)}")
                    print(f"Quantidade de erros: {str(self._erros)}")
                    print(f"Palavra: {mensagem_dados_segredo}")

                    ser.write(mensagem_vidas.encode("utf-8"))
                    ser.write(mensagm_erros.encode("utf-8"))
                    ser.write(
                        mensagem_dados_segredo.encode("utf-8")
                    )  # Palavra com mascara (e com letras corretas)
                    if self._vidas == 0:
                        self._on_active = False
                        print(f"GAME OVER")

                        self._mensagem_game_over = "gameover" + "\n"
                        ser.write(self._mensagem_game_over.encode("utf-8"))
                        game_over_audio = "audio/game_over.wav"

                        pygame.mixer.music.load(game_over_audio)
                        pygame.mixer.music.play()
                        pygame.time.wait(8000)

                    time.sleep(1)

                    if "_" not in self._dados_segredo:
                        self._on_active = False
                        print(f"VOCÊ VENCEU!")

                        self._mensagem_level_complete = "levelcomplete" + "\n"
                        ser.write(self._mensagem_level_complete.encode("utf-8"))
                        level_complete = "audio/level_complete.wav"

                        pygame.mixer.music.load(level_complete)
                        pygame.mixer.music.play()
                        pygame.time.wait(8000)

        except serial.SerialException as e:
            print(f"Algo de errado na porta emulador: {e}")

        except KeyboardInterrupt:
            print("Simulador encerrado")
        finally:
            if "ser" in locals() and ser.is_open:
                ser.close()
                print("Porta do simulador fechado")


if __name__ == "__main__":
    p = ArduinoVirtual(VIRTUAL_ARDUINO_PORT, BAUD_RATE)
