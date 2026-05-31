#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# Adapted from Adeept servosGUI.py for Linux + 14_Control_APP angle.h (#define format)

import sys
import time
import threading as thread
import tkinter as tk
import json
import os
import serial

ANGLE_H_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "14_Control_APP", "angle.h")
DEFAULT_PORT = "/dev/ttyUSB1"

ser = None
ip_stu = 1

def load_angles_from_h():
    """Read current #define values from angle.h"""
    vals = {i: 90 for i in range(13)}
    try:
        with open(ANGLE_H_PATH, "r") as f:
            for line in f:
                for i in range(13):
                    prefix = "#define ANGLE%d " % i
                    if line.startswith(prefix):
                        vals[i] = int(line.strip().split()[-1])
    except Exception:
        pass
    return vals

_a = load_angles_from_h()
init_1  = _a[0];  init_2  = _a[1];  init_3  = _a[2];  init_4  = _a[3]
init_5  = _a[4];  init_6  = _a[5];  init_7  = _a[6];  init_8  = _a[7]
init_9  = _a[8];  init_10 = _a[9];  init_11 = _a[10]; init_12 = _a[11]
init_13 = _a[12]

color_bg   = '#000000'
color_text = '#E1F5FE'
color_btn  = '#0277BD'


def replace_init(define_name, new_num):
    """Update a #define value in angle.h"""
    newline = ""
    prefix = "#define %s " % define_name
    with open(ANGLE_H_PATH, "r") as f:
        for line in f.readlines():
            if line.startswith(prefix):
                line = "%s%d\n" % (prefix, new_num)
            newline += line
    with open(ANGLE_H_PATH, "w") as f:
        f.writelines(newline)


def pwm_show():
    L1.config(text=init_1);   L2.config(text=init_2);   L3.config(text=init_3)
    L4.config(text=init_4);   L5.config(text=init_5);   L6.config(text=init_6)
    L7.config(text=init_7);   L8.config(text=init_8);   L9.config(text=init_9)
    L10.config(text=init_10); L11.config(text=init_11); L12.config(text=init_12)
    L13.config(text=init_13)


def three_function(a, b, c):
    global ser
    if ser is None:
        status_label.config(text="Não conectado!", fg='#FF5252')
        return
    p1 = "{'start':['%s',%s,%s]}\n" % (a, b, c)
    try:
        ser.write(p1.encode("utf-8"))
    except Exception as e:
        ser = None
        status_label.config(text="Conexão perdida. Reconecte.", fg='#FF5252')


def jsonDS(numInput, adjustInput):
    global init_1, init_2, init_3, init_4, init_5, init_6, init_7, init_8
    global init_9, init_10, init_11, init_12, init_13, ser
    vals = [None, init_1, init_2, init_3, init_4, init_5, init_6, init_7,
            init_8, init_9, init_10, init_11, init_12, init_13]
    vals[numInput] = max(0, min(180, vals[numInput] + adjustInput))
    (init_1, init_2, init_3, init_4, init_5, init_6, init_7,
     init_8, init_9, init_10, init_11, init_12, init_13) = vals[1:]
    three_function("angle", numInput - 1, vals[numInput])
    pwm_show()


def wait_connect():
    while True:
        ser.write("{'start':['setup']}\n".encode("utf-8"))
        line = ser.readline()
        if line:
            break


def serial_connect():
    global ser
    com = E1.get()
    try:
        ser = serial.Serial(com, 115200, timeout=1, writeTimeout=10)
        wait_connect()
        status_label.config(text=com + ": Conectado", fg='#69F0AE')
    except Exception as e:
        ser = None
        status_label.config(text=str(e)[:60], fg='#FF5252')


def connect(event):
    if ip_stu == 1:
        sc = thread.Thread(target=serial_connect, daemon=True)
        sc.start()


def initSet(event):
    replace_init("ANGLE0",  init_1)
    replace_init("ANGLE1",  init_2)
    replace_init("ANGLE2",  init_3)
    replace_init("ANGLE3",  init_4)
    replace_init("ANGLE4",  init_5)
    replace_init("ANGLE5",  init_6)
    replace_init("ANGLE6",  init_7)
    replace_init("ANGLE7",  init_8)
    replace_init("ANGLE8",  init_9)
    replace_init("ANGLE9",  init_10)
    replace_init("ANGLE10", init_11)
    replace_init("ANGLE11", init_12)
    replace_init("ANGLE12", init_13)
    status_label.config(text="Salvo em angle.h!", fg='#69F0AE')
    print("Saved to", ANGLE_H_PATH)


def servo_buttons(x, y):
    global L1, L2, L3, L4, L5, L6, L7, L8, L9, L10, L11, L12, L13

    def mkup(n):
        return lambda e: jsonDS(n, 3)
    def mkdn(n):
        return lambda e: jsonDS(n, -3)

    pairs = [
        (1,  "angle0",  "Leg1",  x+100, y),
        (2,  "angle1",  None,    x+200, y),
        (3,  "angle2",  "Leg2",  x+300, y),
        (4,  "angle3",  None,    x+400, y),
        (5,  "angle4",  "Leg3",  x+500, y),
        (6,  "angle5",  None,    x+600, y),
        (7,  "angle6",  "Leg4",  x+100, y+110),
        (8,  "angle7",  None,    x+200, y+110),
        (9,  "angle8",  "Leg5",  x+300, y+110),
        (10, "angle9",  None,    x+400, y+110),
        (11, "angle10", "Leg6",  x+500, y+110),
        (12, "angle11", None,    x+600, y+110),
        (13, "angle12", "Head",  x+700, y+50),
    ]

    labels_refs = [None]*14
    init_vals = [None, init_1, init_2, init_3, init_4, init_5, init_6, init_7,
                 init_8, init_9, init_10, init_11, init_12, init_13]

    for n, name, leg, px, py in pairs:
        if leg:
            tk.Label(root, width=8, text=leg, fg='#FF1493', bg='#212121').place(x=px+50, y=py-35)
        lbl = tk.Label(root, width=8, text=init_vals[n], fg=color_text, bg='#212121')
        lbl.place(x=px, y=py-15)
        labels_refs[n] = lbl
        bi = tk.Button(root, width=8, text=name+'+', fg=color_text, bg=color_btn, relief='ridge')
        bi.place(x=px, y=py+10)
        bi.bind('<ButtonPress-1>', mkup(n))
        bd = tk.Button(root, width=8, text=name+'-', fg=color_text, bg=color_btn, relief='ridge')
        bd.place(x=px, y=py+45)
        bd.bind('<ButtonPress-1>', mkdn(n))

    (L1, L2, L3, L4, L5, L6, L7, L8, L9, L10, L11, L12, L13) = labels_refs[1:]


def loop():
    global root, E1

    root = tk.Tk()
    root.title('Hexapod Servo Calibration')
    root.geometry('850x340')
    root.config(bg=color_bg)

    # Port input
    tk.Label(root, width=10, text='Port:', fg=color_text, bg=color_bg).place(x=25, y=15)
    E1 = tk.Entry(root, show=None, width=16, bg="#37474F", fg='#eceff1')
    E1.insert(0, DEFAULT_PORT)
    E1.place(x=30, y=40)

    btn_conn = tk.Button(root, width=8, height=2, text='Connect', fg=color_text, bg=color_btn, relief='ridge')
    btn_conn.place(x=160, y=25)
    btn_conn.bind('<ButtonPress-1>', connect)
    root.bind('<Return>', connect)

    # SET button
    tk.Label(root, width=23, text='Click after calibrating', fg=color_text, bg=color_bg).place(x=430, y=10)
    btn_set = tk.Button(root, width=8, text='SET', fg=color_text, bg=color_btn, relief='ridge')
    btn_set.place(x=530, y=35)
    btn_set.bind('<ButtonPress-1>', initSet)

    # Status label
    global status_label
    status_label = tk.Label(root, text='Desconectado', fg='#FF5252', bg=color_bg, width=50, anchor='w')
    status_label.place(x=25, y=290)

    # Path info
    tk.Label(root, text='angle.h: ' + ANGLE_H_PATH, fg='#546E7A', bg=color_bg, font=('Courier', 7)).place(x=25, y=315)

    servo_buttons(-70, 120)
    root.mainloop()


if __name__ == '__main__':
    loop()
