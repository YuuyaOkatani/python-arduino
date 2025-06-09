##Este programa python é criado para realziar conexões com pares COM#, com o emulador com0com para realizar teste de arduino. 
##
##Para resumir seu funcionamento, ele tem uma interface gráfica genérica para enviar e receber dados através das portas vituais COM para qualquer periférico, que tenha conexão COM. 
##Tecnolgias: CustomTkinter, Pygame, PySerial.
#Como usar:
##
- Instale o emulador com0com e coloque um par de portas (Ex: COM6 & COM7) no setup (link: https://sourceforge.net/projects/com0com/)
- faça um git clone e coloque nos dois terminais os dois comandos

##No primeiro terminal (porta COM6):
```
cd arduino-python
python homepage.py

```
##No segundo terminal (pode se utilizar arduino real com porta COM7) : 
```
cd arduino-python
python arduino_virtual.py

```

