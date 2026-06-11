# Adeept Hexapod Spider Robot

Robô hexápode de 6 pernas com firmware customizado para Arduino e integração com agentes de IA via MCP.

**Kit oficial:** [www.adeept.com](https://www.adeept.com) — ADA033 Hexapod Spider Robot Kit for Arduino V5.0  
**Código do projeto:** [github.com/MateusSabroza/Spider_adeept](https://github.com/MateusSabroza/Spider_adeept)

---

## Hardware

| Componente | Detalhe |
|---|---|
| Placa | Adeept Pixie Board V3.0 (compatível Arduino UNO) |
| Servos | 13x MG90S — S0-S11 nas pernas (D2-D13), S12 na cabeça (D14) |
| WiFi | ESP8266 integrado |
| LEDs | 6x WS2812 (pino A1) |
| Sensor | Ultrassônico Trig=A2 / Echo=A3 |
| Buzzer | Pino digital |
| Giroscópio | MPU6050 via I2C |

### Mapa de pinos

```
S0(D2) / S1(D3)    → Dianteira Esquerda
S2(D4) / S3(D5)    → Meio Esquerda
S4(D6) / S5(D7)    → Traseira Esquerda
S6(D8) / S7(D9)    → Dianteira Direita
S8(D10)/ S9(D11)   → Meio Direita
S10(D12)/S11(D13)  → Traseira Direita
S12(D14)           → Cabeça
```

---

## Estrutura do projeto

```
14_Control_APP/         — firmware principal
  14_Control_APP.ino    — sketch principal
  angle.h               — offsets de calibração dos 13 servos
  hexpod.h / hexpod.cpp — biblioteca de movimento e LEDs
Adjustment_Servos/      — sketch de calibração individual dos servos
calibrar_servos.py      — script auxiliar de calibração
servosGUI_linux.py      — GUI de calibração (Linux)
spider_mcp.py           — MCP server para controle via Claude
.mcp.json               — configuração do MCP server
```

---

## Configuração do WiFi

Antes de compilar, edite `14_Control_APP/14_Control_APP.ino` e substitua os placeholders:

```cpp
Serial.println("AT+CWJAP=\"SUA_REDE_WIFI\",\"SUA_SENHA_WIFI\"\r\n");
```

O switch da placa deve estar na posição **0** para upload e **1** para operação normal.

---

## Upload do firmware

```bash
# Compilar
arduino-cli compile --fqbn arduino:avr:uno 14_Control_APP/

# Upload (porta pode variar — verificar com `ls /dev/ttyUSB*`)
sudo -E arduino-cli upload --fqbn arduino:avr:uno --port /dev/ttyUSB1 14_Control_APP/
```

---

## Calibração dos servos

1. Faça upload do sketch `Adjustment_Servos/` com o switch em posição 0
2. Abra a GUI de calibração:
   ```bash
   python3 servosGUI_linux.py
   ```
3. Ajuste os sliders de cada servo até o robô ficar nivelado e simétrico
4. Clique em **SET** para salvar os offsets em `14_Control_APP/angle.h`
5. Recompile e faça upload do firmware principal

---

## Comandos TCP

Com o switch em posição **1** e o robô conectado à rede (aguardar ~20s após ligar):

```bash
python3 -c "import socket; s=socket.socket(); s.connect(('IP_DO_ROBO', 4000)); s.send(b'forward')"
```

| Comando | Ação |
|---|---|
| `forward` | Andar para frente |
| `backward` | Andar para trás |
| `left` | Virar à esquerda |
| `right` | Virar à direita |
| `DTS` | Parar |
| `automatic` | Modo desvio automático de obstáculos |
| `steady` | Modo estabilidade (MPU6050) |
| `lightMode` | Ciclo de modos de LED |

---

## MCP Server (integração com Claude)

O `spider_mcp.py` expõe o robô como ferramentas para o Claude via [Model Context Protocol](https://modelcontextprotocol.io).

Configure o IP do robô em `spider_mcp.py`:
```python
ROBOT_HOST = "192.168.x.x"  # IP do robô na sua rede
```

Ferramentas disponíveis: `mover`, `cabeca`, `led`, `modo_desvio`, `modo_seguidor`, `equilibrio`, `buzzer`.

Com o MCP configurado em `.mcp.json`, o Claude pode controlar o robô diretamente por linguagem natural.

---

## Dependências Python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install mcp
```
