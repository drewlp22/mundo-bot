import matplotlib.pyplot as plt

def top_chart(board):
    y = []
    names = []
    dummy = []
    dval = 0

    for val in board:
        names.append(val[0])
        y.append(val[1])
        dummy.append(dval)
        dval += 1
        if dval > 4:
            break

    plt.bar(x=dummy, height=y, tick_label=names)
    plt.savefig('buffer/data.png')