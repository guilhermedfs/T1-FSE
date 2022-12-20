import sys,os,signal
import time
from datetime import datetime
from threading import Thread
import curses
from curses.textpad import rectangle
import socket
import json

from room import Room
from jsonModel import InOutModel

keyboardPress = -1

alarmEnabled = False
alarmeActivated = False

alarmeIncendio = False
rooms = []

validInputs = ['presenca', 'fumaca', 'janela', 'contagem', 'porta', 'dth22']
validOutputs = ['lampada', 'ar-condicionado', 'aspersor']


def drawInterface(stdscr):
    global alarmeIncendio, rooms, validInputs, validOutputs, keyboardPress
    global alarmEnabled, alarmeActivated

    stdscr.clear()
    stdscr.refresh()
    stdscr.nodelay(True)

    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.curs_set(0)

    while(keyboardPress != curses.ascii.ESC):

        stdscr.erase()
        height, width = stdscr.getmaxyx()

        title = f"Endereço do Servidor Central -> {sys.argv[1]}:{sys.argv[2]}"[:width-1]
        title_x = int((width // 2) - (len(title) // 2) - len(title) % 2)
        stdscr.addstr(0, title_x, title, curses.color_pair(1))

        footer = "'Esc' para sair | 'a' para ativar/desativar alarme"
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, footer)
        stdscr.addstr(height-1, len(footer), " " * (width - len(footer) - 1))
        stdscr.attroff(curses.color_pair(3))

        mid_x = width // 2
        subbar_h = 10
        rectangle_h = height - subbar_h
        margin_x = 2
        line = 3

        if(len(rooms) >= 1):
            titleCol1 = f"{rooms[0].nome}"
            titleCon1 = True
            andart = rooms[0].contagem.getValue()
            stdscr.addstr(2, margin_x, f"Temperatura: {rooms[0].temperatura:.1f} Cº", curses.color_pair(2))
            stdscr.addstr(3, margin_x, f"Humidade: {rooms[0].humidade:.1f} %", curses.color_pair(2))
            drawIOInterface(stdscr, line+2, margin_x, rooms[0].inputs)
            drawIOInterface(stdscr, line+4+len(rooms[0].outputs), margin_x, rooms[0].outputs)
            stdscr.addstr(rectangle_h+2, margin_x, f"Pessoas no prédio: {andart}", curses.color_pair(2))
        else:
            titleCol1 = f"Sem conexão!"
            titleCon1 = False
        stdscr.attron(curses.color_pair(4) if titleCon1 == False else curses.color_pair(2))
        stdscr.addstr(1, margin_x, titleCol1)
        stdscr.attroff(curses.color_pair(4) if titleCon1 == False else curses.color_pair(2))

        if(len(rooms) >= 2):
            titleCol2 = f"{rooms[1].nome}"
            titleCon2 = True
            andar2 = rooms[1].contagem.getValue()
            stdscr.addstr(2, int(mid_x//2 + 1)+margin_x, f"Temperatura: {rooms[1].temperatura:.1f} Cº", curses.color_pair(2))
            stdscr.addstr(3, int(mid_x//2 + 1)+margin_x, f"Humidade: {rooms[1].humidade:.1f} %", curses.color_pair(2))
            drawIOInterface(stdscr, line+2, int(mid_x//2 + 1)+margin_x, rooms[1].inputs)
            drawIOInterface(stdscr, line+4+len(rooms[1].outputs), int(mid_x//2 + 1)+margin_x, rooms[1].outputs)
            stdscr.addstr(rectangle_h+3, margin_x, f"Pessoas na {rooms[0].nome}: {andart-andar2}", curses.color_pair(2))
            stdscr.addstr(rectangle_h+4, margin_x, f"Pessoas na {rooms[1].nome}: {andar2}", curses.color_pair(2))
        else:
            titleCol2 = f"Sem conexão!"
            titleCon2 = False
        stdscr.attron(curses.color_pair(4) if titleCon2 == False else curses.color_pair(2))
        stdscr.addstr(1, margin_x+int(mid_x//2 + 1), titleCol2)
        stdscr.attroff(curses.color_pair(4) if titleCon2 == False else curses.color_pair(2))
        
        if(len(rooms) >= 3):
            titleCol3 = f"{rooms[2].nome}"
            andar3 = rooms[2].contagem.getValue()
            stdscr.addstr(2, mid_x + 1 +margin_x, f"Temperatura: {rooms[2].temperatura:.1f} Cº", curses.color_pair(2))
            stdscr.addstr(3, mid_x + 1+margin_x, f"Humidade: {rooms[2].humidade:.1f} %", curses.color_pair(2))
            drawIOInterface(stdscr, line+2, mid_x + 1 + margin_x, rooms[2].inputs)
            drawIOInterface(stdscr, line+4+len(rooms[2].outputs), mid_x + 1 + margin_x, rooms[2].outputs)
            stdscr.addstr(rectangle_h+5, margin_x, f"Pessoas na {rooms[2].nome}: {andar3}", curses.color_pair(2))
        else:
            titleCol3 = f"Sem conexão!"
        stdscr.attron(curses.color_pair(4) if titleCon2 == False else curses.color_pair(2))
        stdscr.addstr(1, margin_x + mid_x + 1, titleCol3)
        stdscr.attroff(curses.color_pair(4) if titleCon2 == False else curses.color_pair(2))

        
        if(len(rooms) >= 4):
            titleCol4 = f"{rooms[3].nome}"
            andar4 = rooms[3].contagem.getValue()
            stdscr.addstr(2, width - int(width/4)+ 1 + margin_x, f"Temperatura: {rooms[3].temperatura:.1f} Cº", curses.color_pair(2))
            stdscr.addstr(3, width - int(width/4)+ 1 + margin_x, f"Humidade: {rooms[3].humidade:.1f} %", curses.color_pair(2))
            drawIOInterface(stdscr, line+2, width - int(width/4)+ 1 + margin_x, rooms[3].inputs)
            drawIOInterface(stdscr, line+4+len(rooms[3].outputs), width - int(width/4)+ 1 + margin_x, rooms[3].outputs)
            stdscr.addstr(rectangle_h+6, margin_x, f"Pessoas na {rooms[3].nome}: {andar4}", curses.color_pair(2))
        else:
            titleCol4 = f"Sem conexão!"
        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(1, width - int(width/4)+ 1 + margin_x, titleCol4)
        stdscr.attroff(curses.color_pair(4))

        stdscr.addstr(rectangle_h+1, margin_x, "Contagem de pessoas")
        stdscr.addstr(rectangle_h+1, margin_x+mid_x, "Alarmes")

        if(alarmeIncendio):
            stdscr.addstr(rectangle_h+2, margin_x+mid_x, f"Alarme de incêndio ativado!", curses.color_pair(6))
        else:
            stdscr.addstr(rectangle_h+2, margin_x+mid_x, f"Alarme desativado!", curses.color_pair(5))

        if(alarmEnabled):
            if(alarmeActivated):
                stdscr.addstr(rectangle_h+3, margin_x+mid_x, f"Alarme acionado!", curses.color_pair(6))
            else:
                stdscr.addstr(rectangle_h+3, margin_x+mid_x, f"Alarme ativado!", curses.color_pair(5))
        else:
            stdscr.addstr(rectangle_h+3, margin_x+mid_x, f"Alarme desativado!    ", curses.color_pair(7))
        stdscr.refresh()
        keyboardPress = stdscr.getch()

        time.sleep(0.09)


def drawIOInterface(stdscr, lineStart: int, margin_x: int, ios: list):
    for tmp_in in ios:
        if(tmp_in.getKey() != None):
            press = f"F{tmp_in.getKey() % curses.KEY_F0}"
            stdscr.addstr(lineStart, margin_x, f"{press}", curses.color_pair(3))
        else:
            press = ''

        valueColor = curses.color_pair(5) if tmp_in.getValue() else curses.color_pair(6)
        stdscr.addstr(lineStart, margin_x+len(press), f"  ", valueColor)
        stdscr.addstr(lineStart, margin_x+len(press)+3, f"{tmp_in.getTag()}", curses.color_pair(2))
        lineStart += 1


def readSocket(con):
    global alarmEnabled, rooms

    room = None
    while True:
        msg = con.recv(1024)
        if not msg: break
        msgs = [tmp+'}' for tmp in msg.decode('utf8').split('}') if tmp]

        for msg in msgs:
            json_object = json.loads(msg)
            if(json_object['mode'] == 'create'):
                if(json_object['type'] == "nome"):
                    room = Room(json_object['tag'])
                    rooms.append(room)
                else:
                    initIO(json_object, room)

            elif(json_object['mode'] == 'update'):
                updateInput(json_object, room)

    con.close() 


def sendSocket(con):
    global keyboardPress, rooms, alarmeIncendio, alarmEnabled, alarmeActivated

    gpio = -1
    value = -1
    while True:
        if(alarmeIncendio):
            enableSprinkler(con)

        time.sleep(0.09)
        if(keyboardPress == -1):
            continue
        elif(keyboardPress == curses.ascii.ESC):
            break
        elif(keyboardPress == ord('a')):
            if(not alarmEnabled):
                enableAlarm()
            else:
                alarmEnabled = False
                alarmeActivated = False

        for tmp in rooms:
            if(keyboardPress == -1): break
            for tmp_io in tmp.outputs:
                if(tmp_io.getKey() == keyboardPress):
                    gpio = tmp_io.getGpio()
                    value = not tmp_io.getValue()
                    if(value):
                        log = 'Ativado'
                    else:    
                        log = 'Desativado'
                    writeLog(f"{log} {tmp_io.getTag()}")
                    tmp_io.setValue(value)
                    keyboardPress = -1
                    break  
        keyboardPress = -1

        if(gpio == -1 and value == -1): continue
        buff = {"gpio":gpio,"value":value}
        nsent = con.send(json.dumps(buff).encode('utf-8'))
        if not nsent: break
        time.sleep(0.5)


def initIO(json_object, andar):
    global rooms, alarmeIncendio, validInputs, validOutputs
    msgIo = InOutModel(json_object['type'], json_object['tag'], json_object['gpio'], json_object['value'])

    if(andar == None):
        pass

    elif json_object['type'] in validInputs:
        for i, tmp in enumerate(rooms):
            if(tmp.nome == andar.nome):
                if(json_object['type'] == 'contagem'):
                    rooms[i].setContagem(msgIo)
                elif(json_object['type'] == 'fumaca'):
                    rooms[i].addInput(msgIo)
                    if(json_object['value'] and not alarmeIncendio):
                        writeLog("Acionado alarme de incêndio")
                    alarmeIncendio = json_object['value']
                else:
                    rooms[i].addInput(msgIo)

    elif json_object['type'] in validOutputs:
        for i, tmp in enumerate(rooms):
            if(tmp.nome == andar.nome):
                msgIo.setKey(curses.KEY_F1)
                curses.KEY_F1 += 1
                rooms[i].addOutput(msgIo)


def updateInput(json_object, andar):
    global rooms, validInputs, alarmeIncendio
    if(andar == None):
        pass

    elif json_object['type'] in validInputs:
        for i, tmp in enumerate(rooms):
            if(tmp.nome == andar.nome):
                if(json_object['type'] == 'fumaca'):
                    alarmeIncendio = json_object['value']
                if(json_object['type'] == 'dth22'):
                    rooms[i].setTemperatura(json_object['temperatura'])
                    rooms[i].setHumidade(json_object['humidade'])
                elif(json_object['type'] == 'contagem'):
                    rooms[i].contagem.setValue(json_object['value'])
                else:
                    for j, in_tmp in enumerate(rooms[i].inputs):
                        if(in_tmp.getGpio() == json_object['gpio']):
                            rooms[i].inputs[j].setValue(json_object['value'])
                if(not alarmeIncendio):
                    for tmp_andar in rooms:
                        for tmp_andar_in in tmp_andar.inputs:
                            if(tmp_andar_in.getType() == 'fumaca'):
                                if(tmp_andar_in.getValue()):
                                    alarmeIncendio = True



def initSocket(enderecoHost: str, porta: int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((enderecoHost, porta))
    sock.listen(1)

    while True:
        con, cliente = sock.accept()
        readSocketThread = Thread(target=readSocket, args=(con,))
        readSocketThread.start()
        sendSocketThread = Thread(target=sendSocket, args=(con,))
        sendSocketThread.start()


def enableSprinkler(con):
    global rooms, alarmeIncendio
    for i, tmp in enumerate(rooms):
        for j, tmp_in in enumerate(tmp.outputs):
            if(tmp_in.getType() == 'aspersor'):
                if(not tmp_in.getValue()):
                    buff = {"gpio":tmp_in.getGpio(),"value":True}
                    con.send(json.dumps(buff).encode('utf-8'))
                    rooms[i].outputs[j].setValue(True)


def enableAlarm():
    global rooms, alarmEnabled, alarmeActivated
    alarmEnabled = not alarmEnabled
    if(alarmEnabled):
        for tmp in rooms:
            for tmp_in in tmp.inputs:
                if(tmp_in.getValue()):
                    alarmEnabled = False
                    break
    if(alarmEnabled):
        alarmeThread = Thread(target=alarmRoutine)
        alarmeThread.start()
    else:
        alarmeActivated = False


def alarmRoutine():
    global rooms, alarmEnabled, alarmeActivated
    while alarmEnabled and not alarmeActivated:
        for tmp in rooms:
            for tmp_in in tmp.inputs:
                if(tmp_in.getValue()):
                    alarmeActivated = True
                    writeLog("Acionado alarme")
                    break
        if not alarmEnabled: break
        time.sleep(0.5)


def writeLog(text: str):
    log = open('logger.csv', 'a')
    log.write(f"{datetime.now()}, {text}\n")
    log.close()


def sigint_handler(signal, frame):
    pass


if __name__ == "__main__":

    signal.signal(signal.SIGINT, sigint_handler)

    if(len(sys.argv) != 3):
        print(f"Use: {sys.argv[0]} <endereço ip> <porta>")
        print(f"Exemplo: {sys.argv[0]} 192.168.0.53 10055")
        os._exit(os.EX_OK)

    socketThread = Thread(target=initSocket, args=(str(sys.argv[1]),int(sys.argv[2]),))
    socketThread.start()

    interfaceThread = Thread(target= curses.wrapper, args=(drawInterface,))
    interfaceThread.start()
    interfaceThread.join()

    os._exit(os.EX_OK)