# Spider Robot - Adeept Hexapod

## Autorização
Autorizado a executar git commits, uploads Arduino e edições de código sem pedir confirmação.

## Hardware
- **Placa**: Adeept Pixie Board V3.0 (compatível Arduino UNO)
- **Servos**: 13 servos — S0-S11 nas pernas (D2-D13), S12 cabeça (D14)
- **Switch**: posição 0 = upload/programação, posição 1 = operação normal (ESP8266 ativo)
- **Porta serial**: `/dev/ttyUSB1` (grupo `uucp` no Arch Linux)
- **WiFi**: ESP8266 — robô conecta na rede Sabroza2, IP `192.168.15.12`, porta TCP 4000
- **AP próprio**: `Adeept_ADA033` (senha: `12345678`), IP `192.168.4.1`

## Componentes presentes / ausentes
| Componente | Status |
|---|---|
| 13 servos D2-D14 | ✅ Funcionando e calibrados |
| OLED display | ❌ Não presente — removido do firmware |
| WS2812 LEDs (5x, pino A3) | ⚠️ Não conectado ou não montado |
| Sensor ultrassônico I2C 0x57 | ⚠️ Status desconhecido |
| MPU6050 (giroscópio) I2C | ⚠️ Status desconhecido |
| Buzzer (pino A2) | ⚠️ Status desconhecido |

## Mapa de pinos (CORRIGIDO)
```
S0=D2, S1=D3, S2=D4, S3=D5, S4=D6, S5=D7
S6=D8, S7=D9, S8=D10, S9=D11, S10=D12, S11=D13
S12=D14 (cabeça)
Buzzer=A2, WS2812=A3, Bateria=A7
```

## Mapa das pernas
```
S0(D2)/S1(D3)   = Dianteira Esquerda  (ANGLE0/ANGLE1)
S2(D4)/S3(D5)   = Meio Esquerda       (ANGLE2/ANGLE3)
S4(D6)/S5(D7)   = Traseira Esquerda   (ANGLE4/ANGLE5)
S6(D8)/S7(D9)   = Dianteira Direita   (ANGLE6/ANGLE7)
S8(D10)/S9(D11) = Meio Direita        (ANGLE8/ANGLE9)
S10(D12)/S11(D13)= Traseira Direita   (ANGLE10/ANGLE11)
S12(D14)        = Cabeça              (ANGLE12)
```

## Comandos Arduino CLI
```bash
# Compilar firmware principal
arduino-cli compile --fqbn arduino:avr:uno /home/msabroza/Nextcloud/Homelab/Spider/14_Control_APP/

# Upload firmware principal (switch em 0)
sudo -E arduino-cli upload --fqbn arduino:avr:uno --port /dev/ttyUSB1 /home/msabroza/Nextcloud/Homelab/Spider/14_Control_APP

# Compilar sketch de calibração
arduino-cli compile --fqbn arduino:avr:uno /home/msabroza/Nextcloud/Homelab/Spider/Adjustment_Servos/

# Upload sketch de calibração (switch em 0)
sudo -E arduino-cli upload --fqbn arduino:avr:uno --port /dev/ttyUSB1 /home/msabroza/Nextcloud/Homelab/Spider/Adjustment_Servos/
```

## Testar via TCP (switch em 1, aguardar 20s após ligar)
```bash
# Parar o robô
python3 -c "import socket; s=socket.socket(); s.settimeout(3); s.connect(('192.168.15.12',4000)); s.send(b'DTS'); s.close()"

# Andar para frente
python3 -c "import socket; s=socket.socket(); s.settimeout(3); s.connect(('192.168.15.12',4000)); s.send(b'forward'); s.close()"

# Testar sensor ultrassônico (LEDs mudam de cor OU robô se move)
python3 -c "import socket; s=socket.socket(); s.settimeout(3); s.connect(('192.168.15.12',4000)); s.send(b'testdist'); s.close()"
```

## GUI de calibração
```bash
python3 /home/msabroza/Nextcloud/Homelab/Spider/servosGUI_linux.py
# Porta: /dev/ttyUSB1, switch em 0
# Lê angle.h automaticamente ao abrir
# Clicar SET salva em 14_Control_APP/angle.h
```

## Problemas conhecidos / pendentes
1. **Sensor ultrassônico**: verificar se está conectado na porta Ultrasonic da placa
2. **WS2812 LEDs**: não respondem a comandos — verificar conexão física
3. **ANGLE6=3** (Dianteira Direita hip): valor muito baixo, quase no limite mecânico
4. **Obstacle avoidance**: não funciona sem sensor ultrassônico conectado
5. **MPU6050**: não testado — necessário para modo de equilíbrio automático

## MCP Server
```bash
# spider_mcp.py conecta via TCP em 192.168.15.12:4000
# Configurado em .mcp.json
# Ferramentas: mover, cabeca, led, modo_desvio, modo_seguidor, equilibrio, buzzer
```

## Arquivos importantes
- `14_Control_APP/14_Control_APP.ino` — firmware principal
- `14_Control_APP/angle.h` — ângulos de calibração dos servos
- `14_Control_APP/servo_move.h` — definição dos pinos dos servos
- `Adjustment_Servos/Adjustment_Servos.ino` — sketch de calibração
- `servosGUI_linux.py` — GUI de calibração (Linux)
- `spider_mcp.py` — MCP server para controle via Claude
