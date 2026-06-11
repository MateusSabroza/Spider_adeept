# Script de Fala — Seminário Hexápode
# Tempo total: ~10 minutos

**Código do projeto:** https://github.com/MateusSabroza/Spider_adeept
**Kit oficial Adeept:** https://www.adeept.com

---

## [Slide 1 — Título] — 20s

"Boa tarde a todos. Vou apresentar o projeto que desenvolvi nos últimos meses: um robô hexápode — seis pernas — que eu montei, programei, e integrei com um modelo de linguagem. Vou mostrar como ele funciona hoje e onde isso pode chegar."

---

## [Slide 2 — O que é este robô?] — 40s

"Um hexápode é um robô com seis pernas que imita a locomoção de insetos. Cada lado tem dois servos: um para mover a perna para frente e para trás, outro para levantar e abaixar. Na cabeça, tem um terceiro eixo com sensor de distância.

O interessante do hexápode é a estabilidade: com seis pernas, ele nunca cai ao levantar três delas ao mesmo tempo — sempre três no chão formando um triângulo de apoio."

> *[mostrar o robô fisicamente se possível]*

---

## [Slide 3 — Hardware: componentes] — 1min

"O cérebro é uma placa compatível com Arduino UNO, chamada Adeept Pixie. Ela controla diretamente os 13 servos — doze nas pernas e um na cabeça.

O que torna o controle remoto possível é o ESP8266, um módulo WiFi integrado à placa. Ele conecta na rede e escuta comandos via TCP.

Tem também seis LEDs endereçáveis RGB que uso como indicadores de estado, um sensor ultrassônico na cabeça para detectar obstáculos, e um buzzer para feedback sonoro."

---

## [Slide 4 — Mapa de pinos e pernas] — 40s

"Cada perna usa dois pinos digitais do Arduino. A distribuição é simétrica: esquerda nos pinos D2 a D7, direita nos pinos D8 a D13, e a cabeça no D14.

Isso importa porque a calibração é individual: cada servo tem uma posição mecânica ligeiramente diferente, então preciso salvar um offset para cada um dos 13 servos."

---

## [Slide 5 — Firmware e calibração] — 1min 10s

"O firmware é escrito em C++ para Arduino e usa uma biblioteca chamada hexpod, que implementa as sequências de marcha — a ordem e o ângulo em que cada servo se move para o robô andar de forma coordenada.

A calibração foi um processo manual: escrevi uma GUI em Python que mostra sliders para cada servo. Eu ajusto visualmente até o robô ficar nivelado e simétrico, e o programa salva os offsets num arquivo chamado angle.h que o firmware lê.

Com isso, tenho cinco modos funcionando: andar para frente e para trás, virar, desviar obstáculos automaticamente, e um modo de estabilidade."

> *[mostrar screenshot da GUI ou o robô andando se tiver vídeo]*

---

## [Slide 6 — Conectividade: ESP8266 + TCP] — 50s

"O controle remoto funciona assim: o robô conecta na rede WiFi da minha casa e abre um servidor TCP na porta 4000. Qualquer programa que mande texto para esse endereço e essa porta controla o robô.

Os comandos são strings simples: 'forward', 'backward', 'left', 'right', 'DTS' para parar. Isso é propositalmente simples — é o protocolo do app oficial Adeept, mas como é TCP puro, qualquer coisa pode mandar comandos: um script Python, um app, ou, como vou mostrar agora, um modelo de linguagem."

---

## [Slide 7 — MCP: o que é?] — 1min

"Para integrar o robô com IA, usei o MCP — Model Context Protocol. É um padrão aberto lançado pela Anthropic em 2024.

A ideia é simples: você define um conjunto de ferramentas — cada uma com nome, descrição e parâmetros. O servidor MCP expõe essas ferramentas para o modelo. Quando o Claude recebe uma tarefa, ele decide qual ferramenta usar e com quais parâmetros, sem que você precise programar essa lógica.

É o mesmo mecanismo que permite que um LLM faça buscas na internet ou consulte um banco de dados — só que aqui, as ferramentas são ações físicas."

---

## [Slide 8 — MCP aplicado ao robô] — 1min 10s

"O spider_mcp.py é o servidor MCP que escrevi. Ele expõe sete ferramentas para o Claude: mover o robô nas quatro direções, girar a cabeça para um ângulo específico, mudar a cor dos LEDs, ativar o modo de desvio automático, e acionar o buzzer.

Na prática, posso digitar para o Claude: 'vire à esquerda e pisque os LEDs em vermelho'. Ele entende a intenção, chama a ferramenta mover com o parâmetro 'left', depois chama a ferramenta led com a cor, e o robô faz isso — sem que eu tenha escrito nenhum código de decisão. Quem decide é o modelo."

> *[mostrar demo ao vivo ou vídeo gravado]*

---

## [Slide 9 — Visão futura: agente autônomo] — 1min

"O que tenho hoje funciona bem, mas tem um gargalo: o Claude só age quando eu digito algo. O loop não é autônomo.

O próximo passo é fechar esse ciclo. O robô tem sensores — ultrassônico, LEDs de estado, e futuramente câmera e giroscópio. Com um computador embarcado, como o Jetson Nano da NVIDIA, dá para rodar um modelo de linguagem localmente, alimentar os dados dos sensores como entrada, e deixar o modelo decidir a próxima ação em loop contínuo. Sem intervenção humana."

---

## [Slide 10 — Isso já existe na indústria] — 50s

"E isso não é especulação. É o que está sendo feito agora.

A Figure AI tem robôs humanoides com LLM embarcado tomando decisões físicas em tempo real. O Spot da Boston Dynamics ganhou integração com GPT-4. O Google publicou o RT-2, um modelo que processa visão e linguagem e gera ações de robô diretamente.

A NVIDIA tem um SDK chamado Isaac ROS projetado especificamente para rodar essa arquitetura no Jetson. O padrão da indústria é uma camada rápida no firmware para reflexos, e uma camada cognitiva no LLM para decisões de alto nível. O meu projeto já segue essa estrutura — o firmware é a camada rápida, o Claude via MCP é a camada cognitiva."

---

## [Slide 11 — Conclusão] — 30s

"Para resumir: montei o robô do zero, calibrei 13 servos, implementei múltiplos modos de movimento, e conectei tudo a um modelo de linguagem via MCP.

O projeto hoje é controlado por linguagem natural. O próximo passo é tornar esse controle autônomo e contínuo, sem depender de entrada humana.

Obrigado — fico à disposição para perguntas."

---

## Dicas de apresentação

- **Demo ao vivo**: se for fazer, tenha um vídeo gravado como backup — WiFi em auditório é imprevisível
- **Mostre o robô fisicamente** nos dois primeiros slides, não só em foto
- **Slide 7 (MCP)**: é o mais abstrato — pause um segundo depois de explicar, pergunte se ficou claro antes de avançar
- **Slide 10 (indústria)**: esse slide legitima o projeto — não pule, ele mostra que você está trabalhando no estado da arte
