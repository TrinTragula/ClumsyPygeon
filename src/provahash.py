board = "rnbqkbnr" \
        "pppppppp" \
        "00000000" \
        "00000000" \
        "00000000" \
        "00000000" \
        "PPPPPPPP" \
        "RNBQKBNR"

table = {}



print board+"00"+"bianco"
key = hash(board+"00"+"bianco")
table[key] = 12

if hash(board+"00"+"banco") not in table:
    print "Ok"
