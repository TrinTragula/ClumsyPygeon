#!/usr/bin/env python
# -*- coding: utf-8 -*-

# DA FARE: CONTROLLARE PEDONI E RE

import sys
from string import ascii_lowercase, ascii_uppercase
from boardvalue import boardvalue
from boardvalue import boardvaluenero

# Rappresentazione della scacchiera
boardbbbbb = "0000000k" \
        "R0R00000" \
        "00000000" \
        "00000000" \
        "00000000" \
        "00000000" \
        "PPPPPPPP" \
        "RNBQKBNR"



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
    trattobackup = tratto
    boardbackup = board

    move(start,end)

    ren = board.index("k")
    reb = board.index("K")

    if tratto == 1 :
        for i in range(len(board)):
            if not islegal( i, reb ):
                move(end,start)
                board = boardbackup
                tratto = trattobackup
                return 1
    if tratto == 0 :
        for i in range(len(board)):
            if not islegal( i, ren ):
                move(end,start)
                board = boardbackup
                tratto = trattobackup
                return 1

    move(end,start)
    board = boardbackup
    tratto = trattobackup
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
                    if end != (start + 8) and end != (start + 16):
                        return 1
                else:
                    if end != (start+8):
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
                and (end != (start + 1 + 1 - 8) or (start/8 != (end/8 -1))) \
                and (end != (start - 8 - 8 + 1) or (start/8 != (end/8 -2))) \
                and (end != (start - 8 - 8 - 1) or (start/8 != (end/8 -2))) \
                and (end != (start - 1 - 1 + 8) or (start/8 != (end/8 -1))) \
                and (end != (start - 1 - 1 - 8) or (start/8 != (end/8 -1))):
                return 1
            return 0

        #############################
        # RE NERO
        #############################
        if board[start] == "k":

            # Il re si muove di uno in qualsivoglia direzione
            if      ((end != (start + 1) and end != (start - 1)) or (start/8 != end/8)) \
                and ( (end != (start + 8)) or (start/8 +1 != end/8)) \
                and ( (end != (start - 8)) or (start/8 -1 != end/8))\
                and ( (end != (start + 9)) or (start/8 +1 != end/8))\
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
            # Il re si muove di uno in qualsivoglia direzione
            if      ((end != (start + 1) and end != (start - 1)) or (start/8 != end/8)) \
                and ( (end != (start + 8)) or (start/8 +1 != end/8)) \
                and ( (end != (start - 8)) or (start/8 -1 != end/8))\
                and ( (end != (start + 9)) or (start/8 +1 != end/8))\
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
            #arrocco
            if arroccoNero == 0:
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
    mossa = (0,0)
    best = -999999999
    boardbackup = board
    trattobackup= tratto
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
            score = - search(depth - 1, -beta, -alpha)
        board = boardb
        tratto = trattob
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

    #arrocco lungo nero
    if start == 4 and end == 2 and board[start] == "k":
        move(4,3)
        move(3,2)
        move(0,1)
        move(1,3)
        return 0
    #arroco corto nero
    if start == 4 and end == 6 and board[start] == "k":
        move(4,5)
        move(5,6)
        move(7,4)
        move(4,5)
        return 0
    #arrocco lungo bianco
    if start == 60 and end == 58 and board[start] == "K":
        move(60,59)
        move(59,58)
        move(56,57)
        move(57,59)
        return 0
    #arroco corto bianco
    if start == 60 and end == 62 and board[start] == "K":
        move(60,61)
        move(61,62)
        move(63,60)
        move(60,61)
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

# routine to make life easier when implemeting uci
def routine(start,end):
    #routine date mosse iniziali e finali
    #così per rendere piu semplice la futura implementazione uci

    if not islegal(start,end):
        if not ischeck(start,end):

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
            if start == 56
                arroccoBiancoCorto += 1

            move(start,end)
        else:
            print "Non puoi, andresti sotto scacco!"
    else:
        print "Illegale, bro"


# Per giocare
def gioco_ascii(lato, deep):
    # Se voglio giocare come bianco in ascii
    global tratto
    global board
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

            sys.stdout.write("Mossa > ")
            try:
                #gioco come bianco
                if tratto == 0:
                    notazione = raw_input() #lamossa
                if tratto == 1:
                    bestscore = search(deep, alpha, beta)
                    lamossa = str(caseToNotation(bestmove[0],bestmove[1]))
                    print "Mossa migliore: " + lamossa
                    notazione = lamossa
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

    # Se voglio giocare come nero in ascii
    tratto = 0
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

            sys.stdout.write("Mossa > ")
            try:
                #gioco come bianco
                if tratto == 0:
                    bestscore = search(deep, alpha, beta)
                    lamossa = str(caseToNotation(bestmove[0],bestmove[1]))
                    print "Mossa migliore: " + lamossa
                    notazione = lamossa
                if tratto == 1:
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

def inizio():
    print "Clumsy Pigeon 0.01"
    print "Per giocare in ascii, digita 'ascii nero|bianco profondita'"
    scelta = raw_input()
    if scelta.partition(' ')[0] == "ascii":
        gioco_ascii(scelta.partition(' ')[2],2)
tratto = 0
inizio()
