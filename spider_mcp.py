#!/usr/bin/env python3
import socket
from mcp.server.fastmcp import FastMCP

ROBOT_HOST = "192.168.x.x"  # substitua pelo IP do robô na sua rede
ROBOT_PORT = 4000

mcp = FastMCP("Spider Robot")


def send_command(cmd: str) -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((ROBOT_HOST, ROBOT_PORT))
        s.send(cmd.encode())
        s.close()
        return f"OK: '{cmd}'"
    except Exception as e:
        return f"Erro: {e}"


@mcp.tool()
def mover(direcao: str) -> str:
    """Move o robô. Direções válidas: frente, tras, esquerda, direita, parar"""
    mapa = {
        "frente": "forward",
        "tras": "backward",
        "esquerda": "left",
        "direita": "right",
        "parar": "DTS",
    }
    cmd = mapa.get(direcao.lower())
    if not cmd:
        return f"Direção inválida. Use: {', '.join(mapa)}"
    return send_command(cmd)


@mcp.tool()
def cabeca(direcao: str) -> str:
    """Gira a cabeça do robô. Direções: esquerda, direita, parar"""
    mapa = {"esquerda": "lookleft", "direita": "lookright", "parar": "LRStop"}
    cmd = mapa.get(direcao.lower())
    if not cmd:
        return f"Direção inválida. Use: {', '.join(mapa)}"
    return send_command(cmd)


@mcp.tool()
def led(r: int, g: int, b: int, efeito: str = "breath") -> str:
    """Controla os LEDs RGB. Efeitos: breath, flowing, rainbow, police"""
    if efeito not in ("breath", "flowing", "rainbow", "police"):
        return "Efeito inválido. Use: breath, flowing, rainbow, police"
    r, g, b = max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))
    return send_command(f"lightMode[{r},{g},{b}]{efeito}")


@mcp.tool()
def modo_desvio(ativar: bool) -> str:
    """Ativa/desativa o modo autônomo de desvio de obstáculos com o sensor ultrassônico"""
    return send_command("automatic" if ativar else "automaticOff")


@mcp.tool()
def modo_seguidor(ativar: bool) -> str:
    """Ativa/desativa o modo seguidor — robô mantém distância de um objeto à frente"""
    return send_command("keepDistance" if ativar else "keepDistanceOff")


@mcp.tool()
def equilibrio(ativar: bool) -> str:
    """Ativa/desativa a auto-estabilização pelo giroscópio MPU6050"""
    return send_command("steady" if ativar else "steadyOff")


@mcp.tool()
def buzzer(ativar: bool) -> str:
    """Ativa/desativa a música do buzzer"""
    return send_command("Buzzer_Music" if ativar else "Buzzer_Music_Off")


if __name__ == "__main__":
    mcp.run()
