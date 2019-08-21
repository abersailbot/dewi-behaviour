import turtle

#specify the starting location
t = turtle.Turtle(52.4174,-4.0858)

for i in range(0,5):

    #head west 500m
    t.left(90)
    t.forward(500)
    t.print()

    #head south 25m
    t.left(90)
    t.forward(25)
    t.print()

    #head east 500m
    t.left(90)
    t.forward(500)
    t.print()

    #head south 25m
    t.right(90)
    t.forward(25)
    t.print()

    #flip back to pointing north to end in same state we started
    t.right(180)

