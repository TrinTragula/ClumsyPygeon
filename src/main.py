#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from string import ascii_lowercase, ascii_uppercase
from boardvalue import boardvalue
from boardvalue import boardvaluenero
from logo import logo

# tabella hash
table = {}

# Rappresentazione della scacchiera
board = "rnbqkbnr" \
        "pppppppp" \
        "00000000" \
        "00000000" \
        "00000000" \
        "00000000" \
        "PPPPPPPP" \
        "RNBQKBNR"

# Chi muove? tratto = 0 bianchi, tratto = 1 neri
tratto = 0

# Per l'arrocco
arroccoNero = 0
arroccoBianco = 0
arroccoNeroLungo = 0
arroccoNeroCorto = 0
arroccoBiancoLungo = 0
arroccoBiancoCorto = 0
isEnpassant = 0

# Lista pezzi
pieces = ["r","n","b","q","k","p","R","N","B","Q","K","P"]
white = ["R","N","B","Q","K","P"]
black = ["r","n","b","q","k","p"]

# Valore dei pezzi
piece_value = {"r" : -5, "n" : -3, "b" : -3 ,"q" : -9,"k" : -9999999 ,"p" : -1, \
               "R" :  5, "N" :  3, "B" :  3 ,"Q" :  9,"K" :  9999999 ,"P" :  1, "0" : 0}

movelist = []

#------------------------------------------------
# Controllo se una posizione porta allo scacco
#------------------------------------------------
def ischeck(start, end):
    global board
    global tratto
    global arroccoNero
    global arroccoBianco
    global arroccoNeroLungo
    global arroccoNeroCorto
    global arroccoBiancoLungo
    global arroccoBiancoCorto
    global isEnpassant

    arroccoNerob = arroccoNero
    arroccoBiancob = arroccoBianco
    arroccoNeroLungob = arroccoNeroLungo
    arroccoNeroCortob = arroccoNeroCorto
    arroccoBiancoLungob = arroccoBiancoLungo
    arroccoBiancoCortob = arroccoBiancoCorto
    isEnpassantb = isEnpassant
    trattob = tratto
    boardb = board
    ren = board.index("k")
    reb = board.index("K")
    if end == ren or end == reb:
        return 1
    move(start,end)
    ren = board.index("k")
    reb = board.index("K")


    if tratto == 1 :
        for i in range(64):
            if not islegal( i, reb ):
                # ripristino le condizioni varie
                board = boardb
                tratto = trattob
                arroccoNero = arroccoNerob
                arroccoBianco = arroccoBiancob
                arroccoNeroLungo = arroccoNeroLungob
                arroccoNeroCorto = arroccoNeroCortob
                arroccoBiancoLungo = arroccoBiancoLungob
                arroccoBiancoCorto = arroccoBiancoCortob
                isEnpassant = isEnpassantb
                return 1
    if tratto == 0 :
        for i in range(64):
            if not islegal( i, ren ):
                # ripristino le condizioni varie
                board = boardb
                tratto = trattob
                arroccoNero = arroccoNerob
                arroccoBianco = arroccoBiancob
                arroccoNeroLungo = arroccoNeroLungob
                arroccoNeroCorto = arroccoNeroCortob
                arroccoBiancoLungo = arroccoBiancoLungob
                arroccoBiancoCorto = arroccoBiancoCortob
                isEnpassant = isEnpassantb
                return 1

    # ripristino le condizioni varie
    board = boardb
    tratto = trattob
    arroccoNero = arroccoNerob
    arroccoBianco = arroccoBiancob
    arroccoNeroLungo = arroccoNeroLungob
    arroccoNeroCorto = arroccoNeroCortob
    arroccoBiancoLungo = arroccoBiancoLungob
    arroccoBiancoCorto = arroccoBiancoCortob
    isEnpassant = isEnpassantb
    return 0

# ---------------------------------------------------
# Funzione per controllare la legalita delle mosse
# data una mossa di inizio ed una di fine
# ---------------------------------------------------
def islegal( start, end ):

    if start == end:
        return 1

    # I numeri devono stare dentro la scacchiera, cristo
    if end > 63 or start > 63 or end < 0 or start < 0: # il pezzo vuole andare oltre la scacchiera
        return 1 #illegale

    # Se muovo un pezzo del colore sbagliato o mangio un mio pezzo, illegale
    if tratto == 0 and board[start] in black:
        return 1
    if tratto == 0 and board[end] in white:
        return 1
    if tratto == 1 and board[start] in white:
        return 1
    if tratto == 1 and board[end] in black:
        return 1


    # Se si vuole muovere una casella vuota, illegale
    if board[start] == "0":
        return 1


 ###################################
 #            PEZZI NERI
 ###################################
    if tratto == 1:

        #############################
        # TORRE NERA
        #############################
        if board[start] == "r":
            # Controllo che si muova in orizzontale o verticale
            if (end % 8 != start % 8) and (start/8 != end/8):
                return 1
            # Controllo che la torre non passi sopra nessun pezzo

            # Mossa veritcale
            if (end % 8) == (start % 8):
                # verso giu
                if start < end:
                    end_line = end / 8
                    start_line = start / 8
                    diff = end_line - start_line
                    for i in range(1,diff):
                        if board[start + i*8] != "0":
                            return 1
                #verso su
                if start > end:
                    end_line = end / 8
                    start_line = start / 8
                    diff = start_line - end_line
                    for i in range(1,diff):
                        if board[start - i * 8] != "0":
                            return 1
            # Mossa orizzontale
            if (start/8 == end/8):
                # verso destra
                if start < end:
                    diff = end - start
                    for i in range(1,diff):
                        if board[start + i] != "0":
                            return 1
                # verso sinistra
                if start > end:
                    diff = start -end
                    for i in range(1,diff):
                        if board[start - i] != "0":
                            return 1
            return 0

        #############################
        # PEDONE NERO
        #############################
        if board[start] == "p":
            # Si muove solo verso giu
            # Dalla zona di partenza possono spostarsi di due
            if board[end] == "0":
                if (start/8) == 1 and (board[(start+8)]=="0"):
                    if end != (start + 8) and end != (start + 16)\
                    and ( end != isEnpassant or (end != (start + 9)\
                     and end!= (start+7)) or ((start/8 != (end/8 - 1) ))):
                        return 1
                else:
                    if end != (start+8)\
                    and ( end != isEnpassant or (end != (start + 9) \
                    and end!= (start+7)) or ((start/8 != (end/8 - 1) ))):
                        return 1
            # Se invece mangia
            else:
                if (end != (start + 9) and end!= (start+7)) or ((start/8 != (end/8 - 1) )):
                    return 1
            return 0

        #############################
        # CAVALLO NERO
        #############################
        if board[start] == "n":
            # Il cavallo si muove a L
            if      (end != (start + 8 + 8 + 1) or (start/8 != (end/8 -2))) \
                and (end != (start + 8 + 8 - 1) or (start/8 != (end/8 -2))) \
                and (end != (start + 1 + 1 + 8) or (start/8 != (end/8 -1))) \
                and (end != (start + 1 + 1 - 8) or (start/8 != (end/8 +1))) \
                and (end != (start - 8 - 8 + 1) or (start/8 != (end/8 +2))) \
                and (end != (start - 8 - 8 - 1) or (start/8 != (end/8 +2))) \
                and (end != (start - 1 - 1 + 8) or (start/8 != (end/8 -1))) \
                and (end != (start - 1 - 1 - 8) or (start/8 != (end/8 +1))):
                return 1
            return 0

        #############################
        # RE NERO
        #############################
        if board[start] == "k":
         # Nel caso sia possibile l'arroco
         if arroccoNero == 0:
            #vari arrocchi possibili
            # Il re si muove di uno in qualsivoglia direzione o arrocca
            if      ( (end != (start + 1)) or (start/8    != end/8)) \
                and ( (end != (start - 1)) or (start/8    != end/8)) \
                and ( (end != (start + 8)) or (start/8 +1 != end/8)) \
                and ( (end != (start - 8)) or (start/8 -1 != end/8)) \
                and ( (end != (start + 9)) or (start/8 +1 != end/8)) \
                and ( (end != (start + 7)) or (start/8 +1 != end/8)) \
                and ( (end != (start - 9)) or (start/8 -1 != end/8)) \
                and ( (end != (start - 7)) or (start/8 -1 != end/8)):

                if arroccoNeroCorto == 0   \
                    and board[5]=="0" and board[6]=="0" \
                    and start == 4 and end == 6\
                    and not ischeck(4,5) and not ischeck(4,6):
                    return 0
                if arroccoNeroLungo == 0   \
                    and board[1]=="0" and board[2]=="0" and board[3]=="0"\
                    and start == 4 and end == 2\
                    and not ischeck(4,1) and not ischeck(4,2) and not ischeck(4,3):
                    return 0
                #se non è una mossa possibile o un arrocco, ritorni uno
                return 1
            return 0

         if arroccoNero != 0:
            #vari arrocchi possibili
            # Il re si muove di uno in qualsivoglia direzione o arrocca
            if      ( (end != (start + 1)) or (start/8    != end/8)) \
                and ( (end != (start - 1)) or (start/8    != end/8)) \
                and ( (end != (start + 8)) or (start/8 +1 != end/8)) \
                and ( (end != (start - 8)) or (start/8 -1 != end/8)) \
                and ( (end != (start + 9)) or (start/8 +1 != end/8)) \
                and ( (end != (start + 7)) or (start/8 +1 != end/8)) \
                and ( (end != (start - 9)) or (start/8 -1 != end/8)) \
                and ( (end != (start - 7)) or (start/8 -1 != end/8)):
                return 1
            return 0


        ##############################
        # ALFIERE NERO
        ##############################
        if board[start] == "b":
            #si muove in diagonale
            #trovo la riga in cui si trova
            rigain = start / 8
            rigaout = end / 8
            diff = abs(rigain - rigaout)
            if diff < 1 or diff > 7:
                return 1
            #si trova su una diagonale
            if end % 7 != start % 7 and end % 9 != start % 9:
                return 1

            # no artefatti matematici (niente righe di riporto)
            if end % 7 == start % 7:
               if start < end :
                      casa = start + diff * 7
                      if casa != end:
                         return 1
               if start > end :
                      casa = start - diff * 7
                      if casa != end:
                         return 1
            if end % 9 == start % 9:
               if start < end :
                      casa = start + diff * 9
                      if casa != end:
                         return 1
               if start > end :
                      casa = start - diff * 9
                      if casa != end:
                         return 1

            #e non deve avere altri pezzi di mezzo
            for i in range(1,diff):
                if end % 7 == start % 7:
                   if start < end :
                      casa = start + i * 7
                      if board[casa] != "0":
                         return 1
                   if start > end :
                      casa = start - i * 7
                      if board[casa] != "0":
                         return 1
                if end % 9 == start % 9:
                   if start < end :
                      casa = start + i * 9
                      if board[casa] != "0":
                         return 1
                   if start > end :
                      casa = start - i * 9
                      if board[casa] != "0":
                         return 1

            return 0


        ##############################
        # REGINA NERA
        ##############################
        if board[start] == "q":
            #si muove come alfiere + torre
            #trovo la riga in cui si trova
            rigain = start / 8
            rigaout = end / 8
            diff = abs(rigain - rigaout)

            #se si può raggiungere
            if      (end % 7 != start % 7) and (end % 9 != start % 9)\
                and (end % 8 != start % 8) and (start/8 != end/8):
                return 1

            # Diagonali

            # no artefatti matematici (niente righe di riporto)
            if end % 7 == start % 7:
               if start < end :
                      casa = start + diff * 7
                      if casa != end:
                         return 1
               if start > end :
                      casa = start - diff * 7
                      if casa != end:
                         return 1
            if end % 9 == start % 9:
               if start < end :
                      casa = start + diff * 9
                      if casa != end:
                         return 1
               if start > end :
                      casa = start - diff * 9
                      if casa != end:
                         return 1

            #e non deve avere altri pezzi di mezzo
            for i in range(1,diff):
                if end % 7 == start % 7:
                   if start < end :
                      casa = start + i * 7
                      if board[casa] != "0":
                         return 1
                   if start > end :
                      casa = start - i * 7
                      if board[casa] != "0":
                         return 1
                if end % 9 == start % 9:
                   if start < end :
                      casa = start + i * 9
                      if board[casa] != "0":
                         return 1
                   if start > end :
                      casa = start - i * 9
                      if board[casa] != "0":
                         return 1

            #Traverse

            # Mossa veritcale
            if (end % 8) == (start % 8):
                # verso giu
                if start < end:
                    end_line = end / 8
                    start_line = start / 8
                    diffo = end_line - start_line
                    for i in range(1,diffo):
                        if board[start + i*8] != "0":
                            return 1
                #verso su
                if start > end:
                    end_line = end / 8
                    start_line = start / 8
                    diffo = start_line - end_line
                    for i in range(1,diffo):
                        if board[start - i * 8] != "0":
                            return 1
            # Mossa orizzontale
            if (start/8 == end/8):
                # verso destra
                if start < end:
                    diffo = end - start
                    for i in range(1,diffo):
                        if board[start + i] != "0":
                            return 1
                # verso sinistra
                if start > end:
                    diffo = start - end
                    for i in range(1,diffo):
                        if board[start - i] != "0":
                            return 1


            return 0

 ###################################
 #            PEZZI BIANCHI
 ###################################
    if tratto == 0:

        #########################
        # TORRE BIANCA
        #########################
        if board[start] == "R":
            # Controllo che si muova in orizzontale o verticale
            if (end % 8 != start % 8) and (start/8 != end/8):
                return 1
            # Controllo che la torre non passi sopra nessun pezzo

            # Mossa veritcale
            if (end % 8) == (start % 8):
                # verso giu
                if start < end:
                    end_line = end / 8
                    start_line = start / 8
                    diff = end_line - start_line
                    for i in range(1,diff):
                        if board[start + i*8] != "0":
                            return 1
                #verso su
                if start > end:
                    end_line = end / 8
                    start_line = start / 8
                    diff = start_line - end_line
                    for i in range(1,diff):
                        if board[start - i * 8] != "0":
                            return 1
            # Mossa orizzontale
            if (start/8 == end/8):
                # verso destra
                if start < end:
                    diff = end - start
                    for i in range(1,diff):
                        if board[start + i] != "0":
                            return 1
                # verso sinistra
                if start > end:
                    diff = start - end
                    for i in range(1,diff):
                        if board[start - i] != "0":
                            return 1
            return 0

        #############################
        # PEDONE BIANCO
        #############################
        if board[start] == "P":
            # Si muove solo verso su
            # Dalla zona di partenza possono spostarsi di due
            if board[end] == "0":
                if (start/8) == 6 and (board[(start-8)]=="0"):
                    if end != (start - 8) and end != (start - 16):
                        return 1
                else:
                    if end != (start-8):
                        return 1
            # Se invece mangia
            else:
                if (end != (start - 9) and end!= (start - 7)) or ((start/8 != end/8 + 1)):
                    return 1
            return 0

        #############################
        # CAVALLO BIANCO
        #############################
        if board[start] == "N":
            # Il cavallo si muove a L
            if      (end != (start + 8 + 8 + 1) or (start/8 != (end/8 -2))) \
                and (end != (start + 8 + 8 - 1) or (start/8 != (end/8 -2))) \
                and (end != (start + 1 + 1 + 8) or (start/8 != (end/8 -1))) \
                and (end != (start + 1 + 1 - 8) or (start/8 != (end/8 +1))) \
                and (end != (start - 8 - 8 + 1) or (start/8 != (end/8 +2))) \
                and (end != (start - 8 - 8 - 1) or (start/8 != (end/8 +2))) \
                and (end != (start - 1 - 1 + 8) or (start/8 != (end/8 -1))) \
                and (end != (start - 1 - 1 - 8) or (start/8 != (end/8 +1))):
                return 1
            return 0

        #############################
        # RE BIANCO
        #############################
        if board[start] == "K":
         # Nel caso sia possibile l'arroco
         if arroccoBianco == 0:
            #vari arrocchi possibili
            # Il re si muove di uno in qualsivoglia direzione o arrocca
            if      ( (end != (start + 1)) or (start/8    != end/8)) \
                and ( (end != (start - 1)) or (start/8    != end/8)) \
                and ( (end != (start + 8)) or (start/8 +1 != end/8)) \
                and ( (end != (start - 8)) or (start/8 -1 != end/8)) \
                and ( (end != (start + 9)) or (start/8 +1 != end/8)) \
                and ( (end != (start + 7)) or (start/8 +1 != end/8)) \
                and ( (end != (start - 9)) or (start/8 -1 != end/8)) \
                and ( (end != (start - 7)) or (start/8 -1 != end/8)):

                if arroccoBiancoCorto == 0   \
                    and board[62]=="0" and board[61]=="0" \
                    and start == 60 and end == 62\
                    and not ischeck(60,61) and not ischeck(60,62):
                    return 0
                if arroccoBiancoLungo == 0   \
                    and board[59]=="0" and board[58]=="0" and board[57]=="0"\
                    and start == 60 and end == 58\
                    and not ischeck(60,59) and not ischeck(60,58) and not ischeck(60,57):
                    return 0
                #se non è una mossa possibile o un arrocco, ritorni uno
                return 1

            return 0


         if arroccoBianco != 0:
            #vari arrocchi possibili
            # Il re si muove di uno in qualsivoglia direzione o arrocca
            if      ( (end != (start + 1)) or (start/8    != end/8)) \
                and ( (end != (start - 1)) or (start/8    != end/8)) \
                and ( (end != (start + 8)) or (start/8 +1 != end/8)) \
                and ( (end != (start - 8)) or (start/8 -1 != end/8)) \
                and ( (end != (start + 9)) or (start/8 +1 != end/8)) \
                and ( (end != (start + 7)) or (start/8 +1 != end/8)) \
                and ( (end != (start - 9)) or (start/8 -1 != end/8)) \
                and ( (end != (start - 7)) or (start/8 -1 != end/8)):
                return 1
            return 0

        ##############################
        # ALFIERE BIANCO
        ##############################
        if board[start] == "B":
            #si muove in diagonale
            #trovo la riga in cui si trova
            rigain = start / 8
            rigaout = end / 8
            diff = abs(rigain - rigaout)
            if diff < 1 or diff > 7:
                return 1
            #si trova su una diagonale
            if end % 7 != start % 7 and end % 9 != start % 9:
                return 1

            # no artefatti matematici (niente righe di riporto)
            if end % 7 == start % 7:
               if start < end :
                      casa = start + diff * 7
                      if casa != end:
                         return 1
               if start > end :
                      casa = start - diff * 7
                      if casa != end:
                         return 1
            if end % 9 == start % 9:
               if start < end :
                      casa = start + diff * 9
                      if casa != end:
                         return 1
               if start > end :
                      casa = start - diff * 9
                      if casa != end:
                         return 1

            #e non deve avere altri pezzi di mezzo
            for i in range(1,diff):
                if end % 7 == start % 7:
                   if start < end :
                      casa = start + i * 7
                      if board[casa] != "0":
                         return 1
                   if start > end :
                      casa = start - i * 7
                      if board[casa] != "0":
                         return 1
                if end % 9 == start % 9:
                   if start < end :
                      casa = start + i * 9
                      if board[casa] != "0":
                         return 1
                   if start > end :
                      casa = start - i * 9
                      if board[casa] != "0":
                         return 1

            return 0


        ##############################
        # REGINA BIANCA
        ##############################
        if board[start] == "Q":
            #si muove come alfiere + torre
            #trovo la riga in cui si trova
            rigain = start / 8
            rigaout = end / 8
            diff = abs(rigain - rigaout)

            #se si può raggiungere
            if      (end % 7 != start % 7) and (end % 9 != start % 9)\
                and (end % 8 != start % 8) and (start/8 != end/8):
                return 1

            # Diagonali

            # no artefatti matematici (niente righe di riporto)
            if end % 7 == start % 7:
               if start < end :
                      casa = start + diff * 7
                      if casa != end:
                         return 1
               if start > end :
                      casa = start - diff * 7
                      if casa != end:
                         return 1
            if end % 9 == start % 9:
               if start < end :
                      casa = start + diff * 9
                      if casa != end:
                         return 1
               if start > end :
                      casa = start - diff * 9
                      if casa != end:
                         return 1

            #e non deve avere altri pezzi di mezzo
            for i in range(1,diff):
                if end % 7 == start % 7:
                   if start < end :
                      casa = start + i * 7
                      if board[casa] != "0":
                         return 1
                   if start > end :
                      casa = start - i * 7
                      if board[casa] != "0":
                         return 1
                if end % 9 == start % 9:
                   if start < end :
                      casa = start + i * 9
                      if board[casa] != "0":
                         return 1
                   if start > end :
                      casa = start - i * 9
                      if board[casa] != "0":
                         return 1

            #Traverse

            # Mossa veritcale
            if (end % 8) == (start % 8):
                # verso giu
                if start < end:
                    end_line = end / 8
                    start_line = start / 8
                    diffu = end_line - start_line
                    for i in range(1,diffu):
                        if board[start + i*8] != "0":
                            return 1
                #verso su
                if start > end:
                    end_line = end / 8
                    start_line = start / 8
                    diffu = start_line - end_line
                    for i in range(1,diffu):
                        if board[start - i * 8] != "0":
                            return 1
            # Mossa orizzontale
            if (start/8 == end/8):
                # verso destra
                if start < end:
                    diffu = end - start
                    for i in range(1,diffu):
                        if board[start + i] != "0":
                            return 1
                # verso sinistra
                if start > end:
                    diffu = start - end
                    for i in range(1,diffu):
                        if board[start - i] != "0":
                            return 1


            return 0



 ########################################################
    # Se ho scordato qualcosa, illegale
    else:
        return 1

# ---------------------------------------------------
# Generatore di mosse
# ---------------------------------------------------
def movegen():
    movelist = []
    for i in range(64):
        if tratto == 1:
            if board[i] in black:
                for j in range(64):
                    if not islegal(i,j):
                        if not ischeck(i,j):
                            movelist.append((i,j))
        if tratto == 0:
            if board[i] in white:
                for k in range(64):
                    if not islegal(i,k):
                        if not ischeck(i,k):
                            movelist.append((i,k))

    return movelist

#----------------------------------------------------
# Valuta la posizione attuale sulla scacchiera
#----------------------------------------------------
def evaluate():
    global board
    value = 0
    if tratto == 0:
        value -= len(movegen())/100000.
        for i in range(64):
            value -= int(piece_value[board[i]])
            if board[i] in ascii_uppercase:
                value -= + int(boardvalue[board[i]][i])/110000.
            if board[i] in ascii_lowercase:
                value -= - int(boardvaluenero[board[i]][i])/110000.

    if tratto == 1:
        value -= len(movegen())/100000.
        for i in range(64):
            value += int(piece_value[board[i]])
            if board[i] in ascii_uppercase:
                value -= - int(boardvalue[board[i]][i])/110000.
            if board[i] in ascii_lowercase:
                value -= + int(boardvaluenero[board[i]][i])/110000.

    return value

#---------------------------------------------------
# Controlla se un pedone è nell'ultima fila
# e puo venire promosso
#---------------------------------------------------
def check_promotion():
    global board
    for i in range(8):
        if board[i] == "P":
            scacchiera = list(board)
            scacchiera[i] = "Q"
            board = "".join(scacchiera)
    for i in range(56,64):
        if board[i] == "p":
            scacchiera = list(board)
            scacchiera[i] = "q"
            board = "".join(scacchiera)

#---------------------------------------------------
# Controlla se è scacco matto
#---------------------------------------------------
def checkmate():
    global tratto
    if not movegen():
        print "Scacco matto!"
        if tratto == 0:
            print "Vince il nero!"
        if tratto == 1:
            print "Vince il bianco!"
        return 1
    return 0


#----------------------------------------------------
# Algoritmo di ricerca mosse negamax
#----------------------------------------------------
alpha = -999999999
beta = 999999999
bestmove=(0,0)
def search(depth, alpha, beta):
    global bestmove
    global board
    global tratto
    global arroccoNero
    global arroccoBianco
    global arroccoNeroLungo
    global arroccoNeroCorto
    global arroccoBiancoLungo
    global arroccoBiancoCorto
    global isEnpassant
    global table

    arroccoNerob = arroccoNero
    arroccoBiancob = arroccoBianco
    arroccoNeroLungob = arroccoNeroLungo
    arroccoNeroCortob = arroccoNeroCorto
    arroccoBiancoLungob = arroccoBiancoLungo
    arroccoBiancoCortob = arroccoBiancoCorto
    isEnpassantb = isEnpassant

    mossa = (0,0)
    best = -999999999
    boardb = board
    trattob= tratto
    listamosse = movegen()
    if not listamosse:
        return -999999999999
    else:
     for i in listamosse:
        boardb = board
        trattob = tratto
        move(i[0], i[1])
        check_promotion()
        if depth == 0:
            score = evaluate()
        else:
            chiave = hash(board + str(depth) + str(tratto))
            if chiave in table:
                    score = table[chiave]
                    print "usato!"
            else:
                    score = - search(depth - 1, -beta, -alpha)

        # ripristino le condizioni varie
        board = boardb
        tratto = trattob
        arroccoNero = arroccoNerob
        arroccoBianco = arroccoBiancob
        arroccoNeroLungo = arroccoNeroLungob
        arroccoNeroCorto = arroccoNeroCortob
        arroccoBiancoLungo = arroccoBiancoLungob
        arroccoBiancoCorto = arroccoBiancoCortob
        isEnpassant = isEnpassantb

        if (score == 999999999999):
            best = score
            mossa = i
            bestmove = mossa
            return best
        if mossa == (0,0):
            mossa = i
        if ( score > best ):
            best = score
            mossa = i
        if ( best > alpha ):
            alpha = best
        if ( alpha >= beta):
            mossa = i
            return alpha
     bestmove = mossa
     #se arrivo qua inserisco la mossa nella table
     chiave = hash(board + str(depth) + str(tratto))
     if chiave not in table:
         table[chiave] = best
     return best

#convert names in unicode chess pieces
def simbol(string):
	if string == "r":
		return "♜"
	if string == "b":
		return "♝"
	if string == "n":
		return "♞"
	if string == "k":
		return "♚"
	if string == "q":
		return "♛"
	if string == "p":
		return "♟"
	if string == "R":
		return "♖"
	if string == "B":
		return "♗"
	if string == "N":
		return "♘"
	if string == "K":
		return "♔"
	if string == "Q":
		return "♕"
	if string == "P":
		return "♙"
	if string == "0":
		return "_"

# ---------------------------------------------------
# Funzione per stampare la scacchiera sullo schermo
# ---------------------------------------------------
def show():

    # Stampa i pezzi ed il contorno
    print "\t" + "#" * 19
    for i in range(8):
        sys.stdout.write("\t#|")
        for j in range(8):
            sys.stdout.write( simbol(board[8*i+j]) + "|")
        sys.stdout.write( "# " + str(8-i)  )
        print ""
    print "\t" + "#" * 19
    sys.stdout.write(" \t ")
    # Stampa le lettere per la notazione
    for i in range(8):
        sys.stdout.write("|" + ascii_lowercase[i])
    sys.stdout.write("|")
    print ""

# From notation to stuff the program eats
def notationToCase(string):
    #prende in input notazione simbolica e restituisce
    #qualcosa di comprensibile dal programma
    colin = string[0]
    rigin = string[1]
    colout = string[2]
    rigout = string[3]
    #numero di colonna
    colonne = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    rigin = int(rigin)
    rigout = int(rigout)
    colin = colonne[colin]
    colout = colonne[colout]
    start = colin + 8 * (8 - rigin)
    end = colout + 8 * (8 - rigout)
    return start, end

# From stuff the program eats to notation
def caseToNotation(i,j):
    colonne = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    mossa = ""
    #trovo riga e colonna inziale e finale
    rigain  = 8 - i/8
    colin = colonne.keys()[colonne.values().index(i % 8)]
    rigaout = 8 - j/8
    colout = colonne.keys()[colonne.values().index(j % 8)]
    mossa += str(colin) + str(rigain) + str(colout) + str(rigaout)
    return mossa

#move the piece
def move(start, end):
    #move a piece in the board
    global board
    global tratto
    global arroccoNero
    global arroccoBianco
    global arroccoNeroLungo
    global arroccoNeroCorto
    global arroccoBiancoLungo
    global arroccoBiancoCorto
    global isEnpassant

    #per la cattura enpassant
    isEnpassant = -1
    if board[start] == "p":
        for i in range(8,16):
            if start == i and (end == (start+16)):
                isEnpassant = i + 8

    if board[start] == "P":
        for i in range(48,56):
            if start == i and (end == (start-16)):
                isEnpassant = i - 8




    #condizioni per l'arrocco
    if board[start] == "k":
        arroccoNero += 1
    if board[start] == "K":
        arroccoBianco += 1
    if start == 0:
        arroccoNeroLungo += 1
    if start == 7:
        arroccoNeroCorto += 1
    if start == 63:
        arroccoBiancoLungo += 1
    if start == 56:
        arroccoBiancoCorto += 1

    #arrocco lungo nero
    if start == 4 and end == 2 and board[start] == "k":
        scacchiera = list(board)
        scacchiera[0] = "0"
        scacchiera[1] = "0"
        scacchiera[2] = "k"
        scacchiera[3] = "r"
        scacchiera[4] = "0"
        board = "".join(scacchiera)
        return 0
    #arroco corto nero
    if start == 4 and end == 6 and board[start] == "k":
        scacchiera = list(board)
        scacchiera[7] = "0"
        scacchiera[6] = "k"
        scacchiera[5] = "r"
        scacchiera[4] = "0"
        board = "".join(scacchiera)
        return 0
    #arrocco lungo bianco
    if start == 60 and end == 58 and board[start] == "K":
        scacchiera = list(board)
        scacchiera[56] = "0"
        scacchiera[57] = "0"
        scacchiera[58] = "K"
        scacchiera[59] = "R"
        scacchiera[60] = "0"
        board = "".join(scacchiera)
        tratto += 1
        if tratto > 1:
            tratto = 0
        return 0
    #arroco corto bianco
    if start == 60 and end == 62 and board[start] == "K":
        scacchiera = list(board)
        scacchiera[63] = "0"
        scacchiera[62] = "K"
        scacchiera[61] = "R"
        scacchiera[60] = "0"
        board = "".join(scacchiera)
        tratto += 1
        if tratto > 1:
            tratto = 0
        return 0

    scacchiera = list(board)
    scacchiera[end] = board[start]
    scacchiera[start] = "0"
    board = "".join(scacchiera)
    check_promotion()
    tratto += 1
    if tratto > 1:
        tratto = 0
    return 0

# routine to make life easier when implemeting xboard
def routine(start,end):
    #routine date mosse iniziali e finali
    #così per rendere piu semplice la futura implementazione uci
    if not islegal(start,end):
        if not ischeck(start,end):
            move(start,end)
        else:
            print "Non puoi, andresti sotto scacco!"
    else:
        print "Illegale, bro"


# Per giocare
def gioco_ascii(lato, deep):
    # Se voglio giocare come bianco in ascii
    global bestmove
    global board
    global tratto
    global arroccoNero
    global arroccoBianco
    global arroccoNeroLungo
    global arroccoNeroCorto
    global arroccoBiancoLungo
    global arroccoBiancoCorto
    global isEnpassant
    global pensa
    global f

    deep = int(deep)
    if lato == "bianco":
        try:
         while(1):
            print "\n"
            show()
            print "Valutazione: " + str(evaluate())
            print "Mosse possibili: " + str(len(movegen())) + str(movegen())
            if checkmate():
                break

            if tratto == 0 :
                print "Tocca al Bianco!"
                print "Cosa vuol muovere, sir?"
            else:
                print "Tocca al Nero!"

            try:
                #gioco come bianco
                if tratto == 0:
                    sys.stdout.write("Mossa > ")
                    notazione = raw_input() #lamossa
                if tratto == 1:
                    bestscore = search(deep, alpha, beta)
                    lamossa = str(caseToNotation(bestmove[0],bestmove[1]))
                    print "Mossa migliore: ", lamossa
                    notazione = lamossa
                if notazione == "exit":
                    print ""
                    print "Arrivederla!"
                    break

                start, end = notationToCase(notazione)
            except Exception, e:
                print e
                print "Notazione non compresa"
                print "Usa notazione algebrica del tipo 'e2e4'"
                continue

            routine(start,end)

        except KeyboardInterrupt:
            print ""
            print "Arrivederla!"

    # Se voglio giocare come nero in ascii
    if lato == "nero":
        try:
         while(1):
            print "\n"
            show()
            print "Valutazione: " + str(evaluate())
            print "Mosse possibili: " + str(len(movegen())) + str(movegen())
            if checkmate():
                break

            if tratto == 0 :
                print "Tocca al Bianco!"

            else:
                print "Tocca al Nero!"
                print "Cosa vuol muovere, sir?"

            try:
                #gioco come bianco
                if tratto == 0:
                    bestscore = search(deep, alpha, beta)
                    lamossa = str(caseToNotation(bestmove[0],bestmove[1]))
                    print "Mossa migliore: " + lamossa
                    notazione = lamossa
                if tratto == 1:
                    sys.stdout.write("Mossa > ")
                    notazione = raw_input() #lamossa
                if notazione == "exit":
                    print ""
                    print "Arrivederla!"
                    break

                start, end = notationToCase(notazione)
            except :
                print "Notazione non compresa"
                print "Usa notazione algebrica del tipo 'e2e4'"
                continue

            routine(start,end)

        except KeyboardInterrupt:
            print ""
            print "Arrivederla!"


pensa = 0
# Comandi xboard
def xboard():
    global bestmove
    global board
    global tratto
    global arroccoNero
    global arroccoBianco
    global arroccoNeroLungo
    global arroccoNeroCorto
    global arroccoBiancoLungo
    global arroccoBiancoCorto
    global isEnpassant
    global pensa
    global f

    stack = []
    while True:
        if stack:
            comando = stack.pop()
        else:
            comando= raw_input()

        f.write(comando)
        f.write("\n")

        if comando == "quit":
            break

        elif comando == 'protover 2':
            print('feature done=0')
            print('feature myname="ClumsyPygeon"')
            print('feature usermove=1')
            print('feature setboard=0')
            print('feature ping=0')
            print('feature sigint=0')
            print('feature variants="normal"')
            print('feature done=1')
            f.write("Risposto a protove 2")
            f.write("\n")

        elif comando == "new":

         f.write("risposto a new")
         f.write("\n")
         # Rappresentazione della scacchiera
         board = "rnbqkbnr" \
                 "pppppppp" \
                 "00000000" \
                 "00000000" \
                 "00000000" \
                 "00000000" \
                 "PPPPPPPP" \
                 "RNBQKBNR"

         # Chi muove? tratto = 0 bianchi, tratto = 1 neri
         tratto = 0

         # Per l'arrocco
         arroccoNero = 0
         arroccoBianco = 0
         arroccoNeroLungo = 0
         arroccoNeroCorto = 0
         arroccoBiancoLungo = 0
         arroccoBiancoCorto = 0
         isEnpassant = 0

         # Lista pezzi
         pieces = ["r","n","b","q","k","p","R","N","B","Q","K","P"]
         white = ["R","N","B","Q","K","P"]
         black = ["r","n","b","q","k","p"]

         # Valore dei pezzi
         piece_value = {"r" : -5, "n" : -3, "b" : -3 ,\
                        "q" : -9,"k" : -9999999 ,"p" : -1, \
                        "R" :  5, "N" :  3, "B" :  3 ,\
                        "Q" :  9,"K" :  9999999 ,"P" :  1, "0" : 0}

         movelist = []
         print "Nuova partita!"


        elif comando == "force":
            pensa = -1

        elif comando == "go":
            pensa = 0
            bestscore = search(2, alpha, beta)
            lamossa = str(caseToNotation(bestmove[0],bestmove[1]))
            start, end = notationToCase(lamossa)
            routine(start,end)
            print "move "+ lamossa
            f.write("move "+ lamossa)
            f.write("\n")

        elif comando.startswith("usermove"):
            comando = comando.split(" ")
            lamossa = comando[1][0:4]
            if len(comando[1]) == 5:
                promozione = comando[1][4]
            #muove la persona
            start, end = notationToCase(lamossa)
            routine(start,end)
            #se non ha ricevuto force muove
            if pensa != -1:
                stack.append('go')
            f.write("Faccio la mossa")
            f.write("\n")

        elif any(comando.startswith(x) for x in \
        ('xboard','random','hard','accepted','level')):
            f.write("Ignoro il comando")
            f.write("\n")
            pass

        else:
            f.write("Errore (comando sconosciuto)")
            f.write("\n")
            pass


# inzio ascii
def inizio():
    print logo
    print "Clumsy Pigeon 0.01"
    print "Per giocare in ascii, digita 'ascii nero|bianco profondita'"
    scelta = raw_input()
    scelta = scelta.split(' ')
    if scelta[0] == "ascii":
        print "\n"*9
        print "Hai scelto di giocare:"
        print "Lato: ", scelta[1]
        print "Profondita: ", scelta[2]
        gioco_ascii(scelta[1],scelta[2])

#inzio xboard
def iniziox():
    global f

    # Disable buffering
    class Unbuffered(object):
        def __init__(self, stream):
            self.stream = stream
        def write(self, data):
            self.stream.write(data)
            self.stream.flush()
        def __getattr__(self, attr):
            return getattr(self.stream, attr)
    sys.stdout = Unbuffered(sys.stdout)

    scelta = raw_input()
    f.write(scelta)
    f.write("\n")
    if scelta == "xboard":
        xboard()
    else:
        inizio()

tratto = 0
#log di cosa accade
f = file('Clumsy_log_xboard.txt', 'w')


iniziox()
