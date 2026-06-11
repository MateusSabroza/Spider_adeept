# Slides — Robô Hexápode: Da Montagem ao Agente Cognitivo

**Código do projeto:** https://github.com/MateusSabroza/Spider_adeept
**Kit oficial Adeept:** https://www.adeept.com

---

## Slide 1 — Título

**Robô Hexápode Adeept**
Da Montagem ao Agente Cognitivo

GitHub: https://github.com/MateusSabroza/Spider_adeept

> Visual: foto do robô montado, destaque nas pernas

---

## Slide 2 — O que é este robô?

- Hexápode: 6 pernas, locomoção por servos
- 3 graus de liberdade por lado: quadril, joelho, tornozelo
- Cabeça giratória com sensor de distância
- Controlado via WiFi em tempo real

> Visual: foto lateral mostrando as pernas + seta apontando cabeça

---

## Slide 3 — Hardware: componentes

| Componente | Função |
|---|---|
| Adeept Pixie V3 (Arduino UNO) | Cérebro do robô — executa o firmware |
| 13 servos MG90S | S0-S11 nas pernas, S12 na cabeça |
| ESP8266 WiFi | Recebe comandos via rede TCP |
| 6x LEDs WS2812 | Indicadores visuais de estado |
| Sensor ultrassônico | Detecção de obstáculos |
| Buzzer | Feedback sonoro |

> Visual: foto da placa com labels, ou diagrama de blocos

---

## Slide 4 — Mapa de pinos e pernas

```
Dianteira Esquerda  → S0(D2) / S1(D3)
Meio Esquerda       → S2(D4) / S3(D5)
Traseira Esquerda   → S4(D6) / S5(D7)
Dianteira Direita   → S6(D8) / S7(D9)
Meio Direita        → S8(D10)/ S9(D11)
Traseira Direita    → S10(D12)/S11(D13)
Cabeça              → S12(D14)
```

> Visual: diagrama do robô visto de cima com as pernas numeradas

---

## Slide 5 — Firmware e calibração

- Escrito em C++ para Arduino
- Biblioteca `hexpod` controla sequências de marcha
- Cada servo tem um **ângulo de offset** salvo em `angle.h`
- Calibração feita com GUI Python — ajuste visual em tempo real
- Modos implementados: andar, ré, virar, desviar obstáculo, estabilidade

> Visual: screenshot da GUI de calibração

---

## Slide 6 — Conectividade: ESP8266 + TCP

- O robô conecta na rede WiFi e escuta na **porta TCP 4000**
- Comandos em texto puro: `forward`, `backward`, `left`, `right`, `DTS`, `automatic`
- Compatível com o app oficial Adeept (Android/iOS)
- Qualquer cliente TCP pode controlar o robô

```bash
# Exemplo: andar para frente via terminal
python3 -c "import socket; s=socket.socket();
  s.connect(('192.168.x.x', 4000)); s.send(b'forward')"
```

> Visual: diagrama simples: celular / computador → WiFi → ESP8266 → Arduino → servos

---

## Slide 7 — MCP: o que é?

**Model Context Protocol** — padrão aberto da Anthropic (2024)

- Define como um LLM pode chamar **ferramentas externas** de forma estruturada
- O modelo recebe a lista de ferramentas disponíveis, decide qual usar, envia parâmetros
- A ferramenta executa e devolve o resultado ao modelo
- Mesmo padrão que ferramentas de busca, bancos de dados, APIs

```
LLM → [decide usar ferramenta] → MCP Server → executa ação → retorna resultado → LLM
```

> Visual: diagrama do fluxo acima

---

## Slide 8 — MCP aplicado ao robô

`spider_mcp.py` — servidor MCP que expõe o robô como ferramentas:

| Ferramenta | O que faz |
|---|---|
| `mover` | frente / ré / esquerda / direita / parar |
| `cabeca` | gira a cabeça para um ângulo |
| `led` | muda cor dos LEDs |
| `modo_desvio` | ativa desvio automático de obstáculos |
| `modo_seguidor` | segue linha no chão |
| `equilibrio` | ativa modo de estabilidade (MPU6050) |
| `buzzer` | emite som |

Claude recebe a lista, decide qual ferramenta usar e com quais parâmetros — sem programação adicional.

> Visual: screenshot do Claude no terminal chamando uma ferramenta e o robô reagindo

---

## Slide 9 — Visão futura: agente autônomo

**Gargalo atual**: Claude só age quando alguém digita no terminal.

**Próximo passo**: fechar o loop — o agente percebe, decide e age sozinho.

```
┌─────────────────────────────────────────────┐
│              Loop Autônomo                  │
│                                             │
│  Sensores ──→ LLM local ──→ MCP tools       │
│  (câmera,     (Jetson Nano)   (mover, LED,  │
│   ultrassônico,               desviar...)   │
│   IMU)            ↑                         │
│                   └── novo estado do robô   │
└─────────────────────────────────────────────┘
```

Hardware candidato: **NVIDIA Jetson Nano/Orin** — GPU embarcada, roda modelos como Llama 3.2 3B localmente, sem internet.

---

## Slide 10 — Isso já existe na indústria

Não é especulação — é o estado atual da robótica:

| Projeto | O que faz |
|---|---|
| **Figure AI** (Figure 01/02) | LLM embarcado tomando decisões físicas em tempo real |
| **Boston Dynamics Spot** | GPT-4 integrado para linguagem natural |
| **Google RT-2** (2023) | Modelo visão-linguagem-ação em robô físico |
| **NVIDIA Isaac ROS** | SDK oficial para exatamente essa arquitetura no Jetson |

O padrão da indústria é **dual-layer**:
- Camada rápida (ms): firmware reativo — desvio, equilíbrio
- Camada cognitiva (s): LLM decide objetivo e estratégia

> Visual: logos das empresas ou foto do Figure 01

---

## Slide 11 — Conclusão

**O que foi construído:**
- Hexápode funcional com 13 servos calibrados
- Firmware com múltiplos modos de movimento
- Servidor MCP integrando o robô ao Claude

**O que vem a seguir:**
- Loop autônomo em Jetson Nano
- Câmera como entrada visual para o LLM
- Robô que age sem intervenção humana

> Visual: foto do robô + diagrama do loop autônomo lado a lado

---

*Total: 11 slides — ~55s por slide em média*
