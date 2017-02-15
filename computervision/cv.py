import cv2
import numpy as np
#from camera import take_snapshot

#Dummy functions until computer-vision is ready
def take_snapshot():
    return 1

def get_board(snapshot):
    return 1

#Class for getting move
class Compvision():
    #Initialize with image of first board
    def __init__(self, snapshot=None):
        if snapshot == None:
            snapshot = take_snapshot()
        self.prev_board = get_board(snapshot)

    #Takes a new snapshot, and compares the previous one with the new, gives out a move
    def get_move(self):
        if self.prev_board:
            snapshot = take_snapshot()
        board = get_board(snapshot)
        move = compare_boards(board)
        return move

    def compare_boards(self, board):
        if np.allclose(self.prev_board, board):
            print 'The two boards are the same'
            return False
        else:
            diff_index = np.where(self.prev_board != board)
            if len(diff_index[0]) == 2:
                color_val_from = self.prev_board[diff_index[0][0]][diff_index[1][0]]
                color_val_to = self.prev_board[diff_index[0][1]][diff_index[1][1]]
                frm =  chr(diff_index[1][0] + 97) +  str(8 - diff_index[0][0])
                to = chr(diff_index[1][1] + 97) + str(8 - diff_index[0][1])
                #If we moved the other way, flip the values
                if color_val_to > 0:
                    (frm, to) = (to, frm)
                return frm + '-' + to
            else:
                print 'an error occured'
                return False


def test(case_number):
    #2 is black, 1 is white, 0 is empty
    prev_board = np.zeros((8,8))
    prev_board[:2][:] = 2
    prev_board[6:][:] = 1
    board = prev_board.copy()
    c = Compvision()
    c.prev_board = prev_board
    
    if case_number == 1:
        board[1][1] = 0
        board[2][1] = 2
        assert c.compare_boards(board) == 'b7-b6', 'Test 1 failed'
        
    elif case_number == 2:
        board[6][0] = 0
        board[5][0] = 1
        assert c.compare_boards(board) == 'a2-a3', 'Test 2 failed'
        
    elif case_number == 3:
        board[6][0] = 0
        board[1][0] = 1
        assert c.compare_boards(board) == 'a2-a7', 'Test 3 failed'

    elif case_number == 4:
        board[1][0] = 0
        board[6][0] = 2
        assert c.compare_boards(board) == 'a7-a2', 'Test 4 failed'
if __name__ == '__main__':

    #Test cases:
    #1: Black moves downwards
    #2: White moves upwards
    #3: white captures black
    #4: Black captures white
    for i in range(1,4):
        test(i)
    print 'All tests passed'
