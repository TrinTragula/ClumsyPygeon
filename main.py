import sys
from string import ascii_lowercase

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

# Lista pezzi
pieces = ["r","n","b","q","k","p","R","N","B","Q","K","P"]
white = ["R","N","B","Q","K","P"]
black = ["r","n","b","q","k","p"]

# Valore dei pezzi
piece_value = {"r" : -5, "n" : -3, "b" : -3 ,"q" : -9,"k" : -9999999 ,"p" : -1, \
               "R" :  5, "N" :  3, "B" :  3 ,"Q" :  9,"K" :  9999999 ,"P" :  1}

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
            if (end % 8) != start and (start/8 != end/8):
                return 1
            # Controllo che la torre non passi sopra nessun pezzo

            # Mossa veritcale
            if (end % 8) == start:
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
                    diff = end - start
                    for i in range(1,diff):
                        if board[start + i] != "0":
                            return 1
            return 0

        #############################
        # PEDONE NERO
        #############################
        if board[start] == "p":
            # Si muove solo verso giu
            # Dalla zona di partenza possono spostarsi di due
            if board[end] == "0":
                if (start/8) == 1:
                    if end != (start + 8) and end != (start + 16):
                        return 1
                else:
                    if end != (start+8):
                        return 1
            # Se invece mangia
            else:
                if end != (start + 9) and end!= (start+7):
                    return 1
            return 0

        #############################
        # CAVALLO NERO
        #############################
        if board[start] == "n":
            # Il cavallo si muove a L
            if      end != (start + 8 + 8 + 1) and end != (start + 8 + 8 - 1) \
                and end != (start + 1 + 1 + 8) and end != (start + 1 + 1 - 8) \
                and end != (start - 8 - 8 + 1) and end != (start - 8 - 8 - 1) \
                and end != (start - 1 - 1 + 8) and end != (start - 1 - 1 - 8):
                return 1
            return 0

        #############################
        # RE NERO
        #############################
        if board[start] == "k":
            # Il re si muove di uno in qualsivoglia direzione
            if      end != (start + 1) and end != (start - 1) \
                and end != (start + 8) and end != (start - 8) \
                and end != (start + 9) and end != (start + 7)  \
                and end != (start - 9) and end != (start - 7):
                return 1
            return 0

        ##############################
        # ALFIERE NERO
        ##############################
        if board[start] == "b":



###################################
#            PEZZI BIANCHI
###################################
    if tratto == 0:

        #########################
        # TORRE BIANCA
        #########################
        if board[start] == "R":
            # Controllo che si muova in orizzontale o verticale
            if (end % 8) != start and (start / 8 != end / 8):
                return 1
            # Controllo che la torre non passi sopra nessun pezzo

            # Mossa veritcale
            if (end % 8) == start:
                # verso giu
                if start < end:
                    end_line = end / 8
                    start_line = start / 8
                    diff = end_line - start_line
                    for i in range(1, diff):
                        if board[start + i * 8] != "0":
                            return 1
                # verso su
                if start > end:
                    end_line = end / 8
                    start_line = start / 8
                    diff = start_line - end_line
                    for i in range(1, diff):
                        if board[start - i * 8] != "0":
                            return 1
            # Mossa orizzontale
            if (start / 8 == end / 8):
                # verso destra
                if start < end:
                    diff = end - start
                    for i in range(1, diff):
                        if board[start + i] != "0":
                            return 1
                # verso sinistra
                if start > end:
                    diff = end - start
                    for i in range(1, diff):
                        if board[start + i] != "0":
                            return 1
            return 0


        #############################
        # PEDONE BIANCO
        #############################
        if board[start] == "P":
            # Si muove solo verso su
            # Dalla zona di partenza possono spostarsi di due
            if board[end] == "0":
                if (start/8) == 6:
                    if end != (start - 8) and end != (start - 16):
                        return 1
                else:
                    if end != (start-8):
                        return 1
            # Se invece mangia
            else:
                if end != (start - 9) and end!= (start - 7):
                    return 1
            return 0

        #############################
        # CAVALLO BIANCO
        #############################
        if board[start] == "N":
            # Il cavallo si muove a L
            if end != (start + 8 + 8 + 1) and end != (start + 8 + 8 - 1) \
                    and end != (start + 1 + 1 + 8) and end != (start + 1 + 1 - 8) \
                    and end != (start - 8 - 8 + 1) and end != (start - 8 - 8 - 1) \
                    and end != (start - 1 - 1 + 8) and end != (start - 1 - 1 - 8):
                return 1
            return 0

        #############################
        # RE BIANCO
        #############################
        if board[start] == "K":
            # Il re si muove di uno in qualsivoglia direzione
            if end != (start + 1) and end != (start - 1) \
                    and end != (start + 8) and end != (start - 8) \
                    and end != (start + 9) and end != (start + 7) \
                    and end != (start - 9) and end != (start - 7):
                return 1
            return 0

########################################################
    # Se ho scordato qualcosa, illegale
    else:
        return 1


# Debugging da cancellare
tratto = 1
print islegal(1,11)
print board[1]
print board[11]



# ---------------------------------------------------
# Funzione per stamapre la scacchiera sullo schermo
# ---------------------------------------------------

def show():

    # Stampa i pezzi ed il contorno
    print "#" * 19
    for i in range(8):
        sys.stdout.write("# ")
        for j in range(8):
            sys.stdout.write(board[8*i+j] + " ")
        sys.stdout.write( "# " + str(8-i)  )
        print ""
    print "#" * 19
    sys.stdout.write(" ")
    # Stampa le lettere per la notazione
    for i in range(8):
        sys.stdout.write("|" + ascii_lowercase[i])
    sys.stdout.write("|")








show()