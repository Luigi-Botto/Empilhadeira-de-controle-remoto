from machine import UART, Pin
import time

# --- CONFIGURAÇÃO DE HARDWARE ---

# UART0 (Bluetooth HC08) nos pinos GP16 (TX) e GP17 (RX)
uart = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17, Pin.IN, Pin.PULL_UP))

# Motores (Ponte H nas GPIOs 2, 3, 4 e 5)
# Convencionado: Motor 1 = Lado Esquerdo, Motor 2 = Lado Direito
motor1_a = Pin(2, Pin.OUT)
motor1_b = Pin(3, Pin.OUT)
motor2_a = Pin(4, Pin.OUT)
motor2_b = Pin(5, Pin.OUT)

# LEDs nas portas 27 e 28
led_d2 = Pin(27, Pin.OUT)
led_d1 = Pin(28, Pin.OUT)
led_ligado = False # Variável para controlar o estado (Push ON/OFF)


# --- LOOP PRINCIPAL ---
while True:
    if uart.any():
        dados_recebidos = uart.read()
        
        try:
            # Decodifica e limpa o comando recebido
            comando = dados_recebidos.decode('utf-8').strip()
            # print("Comando recebido:", comando)
            
            # ==========================================
            #   CONTROLE DA TRAÇÃO (FRENTE / TRÁS / PARAR)
            # ==========================================
            if 'Y' in comando:
                # Vai para Frente (Ambos os motores giram para frente)
                motor1_a.value(0)
                motor1_b.value(1)
                motor2_a.value(0)
                motor2_b.value(1)
                
            elif 'A' in comando:
                # Vai para Trás / Ré (Ambos os motores giram para trás)
                motor1_a.value(1)
                motor1_b.value(0)
                motor2_a.value(1)
                motor2_b.value(0)
                
            elif 'U' in comando:
                # Para todos os motores
                motor1_a.value(0)
                motor1_b.value(0)
                motor2_a.value(0)
                motor2_b.value(0)

            # ==========================================
            #   CONTROLE DA DIREÇÃO (DIFERENCIAL DE MOTORES)
            # ==========================================
            elif 'X' in comando:
                # Vira para a Direita: Liga motor esquerdo (1), desliga direito (2)
                motor1_a.value(0)
                motor1_b.value(1)
                motor2_a.value(1)
                motor2_b.value(0)
                
            elif 'B' in comando:
                # Vira para a Esquerda: Liga motor direito (2), desliga esquerdo (1)
                motor1_a.value(1)
                motor1_b.value(0)
                motor2_a.value(0)
                motor2_b.value(1)
                
            elif 'D' in comando:
                # Soltou o botão de curva: Para ambos os motores
                motor1_a.value(0)
                motor1_b.value(0)
                motor2_a.value(0)
                motor2_b.value(0)

            # ==========================================
            #   CONTROLE DOS LEDS (PUSH ON/OFF)
            # ==========================================
            if 'L' in comando:
                # Inverte o estado atual do LED
                led_ligado = not led_ligado
                
                if led_ligado:
                    led_d1.value(1)
                    led_d2.value(1)
                else:
                    led_d1.value(0)
                    led_d2.value(0)

        except Exception as e:
            # Ignora erros de leitura do Bluetooth para não travar o carro
            pass

    # Resposta rápida (20 milissegundos)
    time.sleep(0.02)