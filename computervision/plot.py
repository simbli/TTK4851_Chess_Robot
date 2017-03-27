import numpy as np
import matplotlib.pyplot as plt

def plot_array(board):
    for i in range(8):
        for j in range(8):
            if board[j,i] == 0:
                pass
            elif board[j,i] == 1:
                plt.plot(i,7-j, 'yo', markersize=12)
            elif board[j,i] == 2:
                plt.plot(i,7-j, 'ko', markersize=12)
            else:
                print 'something is off'
    plt.show()

if __name__ == '__main__':
    plot_array()
