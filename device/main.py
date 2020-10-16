# Program Name: main.py
# Purpose: 
# Coder: Ramon Gnan Garcia - 0926596
# Date: May 18, 2020

from serial_interface import *
from calculations import Calculations
from graph import Graph
from collections import deque

def main():
    ser_arduino = SerialInterface(port = "COM9")
    ser_arduino.connect()
    ser_gauge = SerialInterface(port = "COM10", baudrate = 9600)
    ser_gauge.connect()

    g_command = "1\r"
    boltNum = 1
    gr = Graph()
    calc = Calculations()

    max_dim = gr.max_values
    min_dim = gr.min_values

    while True:
        user_input = int(input("Digite o comando (1: Medir; 2: Resetar Servo; -9: Sair): "))

        if user_input == -9:
            break
        elif user_input == 1:
            print("Scanning...\n")

            ser_gauge.__try_again = 0
            response_list = []
            dim_counter = 0

            while True:
                if dim_counter == 175:
                    break

                ser_gauge.send_request(g_command)
                ser_gauge.__command_len = len(g_command)

                while True:
                    e, response = ser_gauge.read_response()

                    if e != ErrorCode.TryAgain:

                        response_list.append(float(response))
                        dim_counter += 1
                        break
                    if e == ErrorCode.FatalError:
                        break
                    if ser_gauge.__try_again == 10:
                        break

                    ser_gauge.__try_again += 1

                if e == ErrorCode.FatalError:
                    exit()

                ser_arduino.send_request("RotateCounterClockwise\n")

            response_list = calc.normalize_dimensions(response_list)

            if calc.check_dimensions(response_list, max_dim, min_dim) == True:
                print("#### REPROVADO ####\n")
                gr.set_title = "Lingueta LW2H"
                gr.set_y_values = response_list
                gr.plot_graph()
            else:
                print("#### APROVADA ####\n")

        elif user_input == 2:
            ser_arduino.send_request("ResetServo\n")

main()
