#!/usr/bin/env python3
"""
Calibração interativa dos servos do Spider Robot.
Requer: sketch Adjustment_Servos.ino gravado na placa, switch em posição 0.
"""
import serial
import json
import time

PORT = "/dev/ttyUSB0"
BAUD = 115200

NOMES = {
    0: "Esq1-A",  1: "Esq1-B",
    2: "Esq2-A",  3: "Esq2-B",
    4: "Esq3-A",  5: "Esq3-B",
    6: "Dir1-A",  7: "Dir1-B",  # pata dianteira direita
    8: "Dir2-A",  9: "Dir2-B",
    10: "Dir3-A", 11: "Dir3-B",
    12: "Cabeça",
}

angulos = {i: 90 for i in range(13)}


def enviar(ser, servo_id, angulo):
    angulo = max(0, min(180, angulo))
    cmd = json.dumps({"start": ["angle", servo_id, angulo]}) + "\n"
    ser.write(cmd.encode())
    angulos[servo_id] = angulo


def main():
    ser = serial.Serial(PORT, BAUD, timeout=2)
    time.sleep(2)
    print("Conectado. Todos os servos em 90°.\n")
    print("Comandos: <servo> <ângulo>  |  +<servo>  |  -<servo>  |  salvar  |  sair")
    print("Exemplo: '6 75' define servo 6 para 75°")
    print("Exemplo: '+6' aumenta servo 6 em 5°\n")

    for i in range(13):
        enviar(ser, i, 90)

    while True:
        try:
            linha = input(f"servo> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if linha in ("sair", "q"):
            break

        if linha == "salvar":
            print("\nColoque estes valores em angle.h:\n")
            for i, a in angulos.items():
                print(f"  #define ANGLE{i} {a}  // {NOMES[i]}")
            continue

        if linha.startswith("+") and linha[1:].isdigit():
            sid = int(linha[1:])
            enviar(ser, sid, angulos[sid] + 5)
            print(f"  S{sid} ({NOMES[sid]}) = {angulos[sid]}°")
            continue

        if linha.startswith("-") and linha[1:].isdigit():
            sid = int(linha[1:])
            enviar(ser, sid, angulos[sid] - 5)
            print(f"  S{sid} ({NOMES[sid]}) = {angulos[sid]}°")
            continue

        partes = linha.split()
        if len(partes) == 2 and partes[0].isdigit() and partes[1].isdigit():
            sid, ang = int(partes[0]), int(partes[1])
            if 0 <= sid <= 12:
                enviar(ser, sid, ang)
                print(f"  S{sid} ({NOMES[sid]}) = {ang}°")
            else:
                print("  Servo inválido (0-12)")
            continue

        print("  Comando não reconhecido.")

    ser.close()
    print("\nFinalizado.")


if __name__ == "__main__":
    main()
