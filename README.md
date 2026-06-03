# Carrinho de Controle Remoto BLE - Raspberry Pi Pico

Este repositório contém os arquivos de hardware, firmware e documentação técnica para o desenvolvimento de um carrinho de controle remoto controlado via smartphone, projetado como parte da disciplina de Microcontroladores. O sistema utiliza o microcontrolador **Raspberry Pi Pico**, comunicação via **Bluetooth Low Energy (BLE)** e uma estrutura robusta montada sobre um chassi de **MDF** com placas de circuito impresso (PCI) customizadas.

---

## 📋 Sumário
1. [Visão Geral do Projeto](#-visão-geral-do-projeto)
2. [Arquitetura do Sistema](#-arquitetura-do-sistema)
3. [Especificações de Hardware](#-especificações-de-hardware)
4. [Mapeamento de Pinos (GPIO)](#-mapeamento-de-pinos-gpio)
5. [Evolução do Design Mecânico e PCI](#-evolução-do-design-mecânico-e-pci)
6. [Firmware e Protocolo de Comunicação](#-firmware-e-protocolo-de-comunicação)
7. [Estrutura do Repositório](#-estrutura-do-repositório)
8. [Orçamento do Projeto](#-orçamento-do-projeto)
9. [Como Executar o Projeto](#-como-executar-o-projeto)

---

## 🔍 Visão Geral do Projeto
O objetivo do projeto consiste na construção de um veículo terrestre de quatro rodas motrizes controlado remotamente através de um dispositivo móvel com sistema operacional **iOS**. 

A interface sem fio é estabelecida por meio do módulo Bluetooth BLE **HC-08**, responsável por realizar a ponte de comunicação entre o smartphone e o Raspberry Pi Pico. No ambiente iOS, é utilizado o aplicativo **BlackBLE** da RoboCore (adquirido por R$ 4,90), configurado para transmitir pacotes de dados baseados em caracteres simples em letras maiúsculas para o acionamento de direções e periféricos.

---

## 🛠 Arquitetura do Sistema
O fluxo elétrico e de sinais do protótipo segue uma topologia planejada para garantir níveis estáveis de tensão e proteção das portas lógicas do microcontrolador. Uma representação visual completa dessa estrutura está disponível no arquivo `diagrama_blocos.png` localizado na raiz do repositório.

### Fluxo de Potência e Conversão de Sinais:
1. **Fonte de Alimentação Primária:** O circuito é alimentado por uma bateria de lítio com tensão nominal de **7,2 Volts**.
2. **Regulação Buck (Step-Down):** A tensão da bateria é rebaixada e estabilizada por um conversor regulador **LM2596**, configurado para fornecer uma saída constante de **5V**.
3. **Alimentação da Lógica:** O Raspberry Pi Pico recebe energia de forma direta através do pino **VSYS**, utilizando a linha regulada de 5V vinda do step-down.
4. **Conversão de Nível Lógico:** Devido ao fato de o Raspberry Pi Pico operar nativamente com sinais lógicos de **3,3V** e a ponte H **L298N** requerer sinais de **5V** em suas linhas de controle para garantir o acionamento correto dos transistores, foi integrado um **Conversor de Nível Lógico Bidirecional**. O barramento de alta tensão (*High Voltage* - HV) deste módulo conversor é alimentado pelos 5V provenientes da saída do regulador step-down.

---

## ⚙️ Especificações de Hardware

Abaixo encontra-se a listagem detalhada dos principais componentes que integram o hardware do projeto:

| Componente | Função Principal | Especificação / Observação |
| :--- | :--- | :--- |
| **Raspberry Pi Pico** | Unidade de processamento central | Baseado no chip RP2040, operação a 3,3V |
| **Módulo HC-08** | Módulo de comunicação sem fio | Bluetooth Low Energy (BLE), interface serial UART |
| **Ponte H L298N** | Driver de potência para motores | Controle de até 2 canais independentes de corrente |
| **Motores DC (x4)** | Atuadores de tração mecânica | Ligados em paralelo (2 por canal da Ponte H) por lateral |
| **Conversor de Nível Lógico** | Interfaceamento de tensão de dados | Shifter bidirecional de sinal (3,3V para 5V) |
| **Módulo LM2596** | Regulador de tensão Step-Down | Conversor Buck DC-DC ajustado para saída estável de 5V |
| **Bateria de Lítio** | Armazenamento de energia | Tensão de operação de 7,2V |
| **LEDs de Alto Brilho (x2)** | Sistema de iluminação (Faróis) | Conectados em canais independentes (ON/OFF via app) |
| **Chassi Mecânico** | Estrutura física do veículo | Base em MDF com 3mm de espessura |

---

## 📌 Mapeamento de Pinos (GPIO)

As conexões físicas foram estruturadas no circuito impresso e inicializadas no firmware conforme o mapeamento a seguir:

| Periférico / Linha | Função do Pino | Pino no Raspberry Pi Pico | Configuração Digital | Detalhes Técnicos |
| :--- | :--- | :--- | :--- | :--- |
| **Interface UART0 (HC-08)** | Transmissão de Dados (TX) | **GPIO 16** | Saída (`Pin.OUT`) | Conectado diretamente ao RX do HC-08 |
| **Interface UART0 (HC-08)** | Recepção de Dados (RX) | **GPIO 17** | Entrada com Pull-Up (`Pin.IN, Pin.PULL_UP`) | Monitora dados vindos do TX do HC-08 |
| **Ponte H (Lado Esquerdo)** | Motor 1 - Terminal A | **GPIO 2** | Saída (`Pin.OUT`) | Sinal condicionado no Shifter para 5V |
| **Ponte H (Lado Esquerdo)** | Motor 1 - Terminal B | **GPIO 3** | Saída (`Pin.OUT`) | Sinal condicionado no Shifter para 5V |
| **Ponte H (Lado Direito)** | Motor 2 - Terminal A | **GPIO 4** | Saída (`Pin.OUT`) | Sinal condicionado no Shifter para 5V |
| **Ponte H (Lado Direito)** | Motor 2 - Terminal B | **GPIO 5** | Saída (`Pin.OUT`) | Sinal condicionado no Shifter para 5V |
| **Farol Esquerdo (D1)** | Acionamento do LED | **GPIO 28** | Saída (`Pin.OUT`) | Estado lógico controlado via comando BLE |
| **Farol Direito (D2)** | Acionamento do LED | **GPIO 27** | Saída (`Pin.OUT`) | Estado lógico controlado via comando BLE |

---

## 📐 Evolução do Design Mecânico e PCI

### Transição do Sistema de Esterço (Nota de Projeto)
O escopo inicial de engenharia contemplava um mecanismo de direção nas rodas dianteiras baseado no acionamento por um servo motor **MG996R**. A Placa de Circuito Impresso (PCI) foi desenvolvida, impressa e finalizada prevendo as trilhas de dados e alimentação dedicadas a este atuador.

Entretanto, nos ensaios mecânicos de integração, a geometria de esterço projetada apresentou falhas estruturais e travamentos na base de MDF. Como solução de contorno, a equipe optou pela substituição do modelo mecânico tradicional por uma configuração de **direção diferencial (skid-steer / tipo tanque)** utilizando quatro rodas motorizadas.

### Lógica de Curvas e Disposição dos Motores:
* **Conexão Mecânica:** Embora a ponte H L298N possua saídas de potência nominais para apenas dois motores, os quatro motores foram associados em pares paralelos. Os motores de uma mesma lateral pertencem ao mesmo canal de saída da ponte H (e não ao mesmo eixo transversal), permitindo o movimento conjunto de cada lado do veículo.
* **Operação de Curvas:** As manobras são feitas invertendo o sentido de rotação relativo entre as laterais:
  * **Giro à Esquerda:** Lateral direita movimenta-se para frente enquanto a lateral esquerda movimenta-se para trás.
  * **Giro à Direita:** Lateral esquerda movimenta-se para frente enquanto a lateral direita movimenta-se para trás.

*Nota de Design:* O circuito impresso finalizado (PCI) mantém as trilhas e o footprint originais destinados ao servo motor MG996R. Essa característica foi preservada como histórico de desenvolvimento e viabilidade de upgrades mecânicos futuros.

---

## 💻 Firmware e Protocolo de Comunicação

O ambiente lógico do sistema foi desenvolvido sob a linguagem **MicroPython**, utilizando o software **Thonny IDE** para gravação e depuração direta no microcontrolador.

### Protocolo Serial BLE:
A comunicação por Bluetooth baseia-se na escuta constante do barramento `UART(0)`. O aplicativo móvel *BlackBLE* envia strings contendo caracteres simples em **letras maiúsculas** de forma imediata à interação do usuário. O código realiza a leitura desses caracteres e altera as tabelas de verdade das portas lógicas associadas aos pinos `motor1_a`, `motor1_b`, `motor2_a` e `motor2_b` instantaneamente.

### Funcionamento dos Faróis:
Os dois LEDs de sinalização frontal (conectados às GPIOs 27 e 28) operam sob uma lógica assíncrona de alternância (*Toggle Button*). Um botão ON/OFF dedicado no painel do aplicativo envia os comandos específicos de ativação e desativação, mantendo os faróis ligados ou desligados independentemente do estado de translação dos motores.

---

## 📁 Estrutura do Repositório

* 📄 **`diagrama_blocos.png`**: Imagem esquemática detalhando a arquitetura interna e interconexão de blocos do circuito.
* 📄 **`Design_PCI.png`**: Desenho da placa para impressão.
* 📄 **`Esquematico_eletrico.png`**: Imagem esquemática do circuito no KiCad.
* 📄 **`main.py`** *(ou arquivo de código equivalente)*: Código-fonte em MicroPython que roda diretamente no Raspberry Pi Pico.
* 📄 **`README.md`**: Este arquivo de documentação técnica localizado na raiz do repositório.

---

## 💰 Orçamento do Projeto

Abaixo está a relação de custos dos componentes adquiridos para a montagem do protótipo:

| Componente / Material | Quantidade | Custo Estimado (R$) |
| :--- | :---: | :--- |
| Raspberry Pi Pico | 1 | 30,00 |
| Módulo Bluetooth HC-08 | 1 | 35,00 |
| Kit de Baterias (Pilhas Lítio) | 1 | 50,00 |
| Motores DC | 4 | 30,00 |
| Conversor de Nível Lógico | 1 | 25,00 |
| Ponte H L298N | 1 | 20,00 |
| Módulo Step-Down LM2596 | 1 | 7,50 |
| LEDs de Alto Brilho | 2 | 5,00 |
| Resistores | 2 | 0,20 |
| Placa de Circuito Impresso (PCI) | 1 | *Não determinado* |
| Chassi em MDF (3mm) | 1 | *Não determinado* |
| **Custo Total Parcial** | | **R$ 202,70** |

---

## 🚀 Como Executar o Projeto

1. **Validação da Alimentação:** Antes de conectar as saídas às portas digitais do Pico, verifique com um multímetro se a saída do módulo Step-Down LM2596 está ajustada estritamente para **5V** para não danificar o microcontrolador.
2. **Gravação do Firmware:** Abra a IDE Thonny, carregue o arquivo de código fonte, selecione o interpretador correto para o Raspberry Pi Pico e armazene o script diretamente na memória interna do dispositivo.
3. **Operação e Pareamento:** Inicialize a alimentação do circuito por meio da bateria de 7,2V. Abra o aplicativo **BlackBLE** em seu dispositivo iOS, realize o escaneamento físico e conecte-se ao módulo **HC-08**. Configure os botões gráficos para disparar os caracteres maiúsculos definidos para cada comando.
