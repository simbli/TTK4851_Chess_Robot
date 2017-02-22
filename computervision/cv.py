import cv2
import numpy as np
#from camera import take_snapshot

#Dummy functions until computer-vision is ready
def take_snapshot():
    return 1

def get_board(snapshot):
    return True

#Class for getting move
class Compvision():
    #Initialize with image of first board
    def __init__(self, snapshot=None):
        if snapshot == None:
            snapshot = take_snapshot()
        self.prev_board = get_board(snapshot)
        self.board_to_compare = None
    #Takes a new snapshot, and compares the previous one with the new, gives out a move
    def get_move(self):
        #Code here will be added
        #if self.prev_board == None:
        #snapshot = take_snapshot()
        #board = get_board(snapshot)
        move = self.compare_boards()
        return move

    def check_if_move_is_correct(self, move_to_check):
        move = self.get_move()
        if move == move_to_check:
            print 'Move is correct'
            return True
        else:
            print 'Move is false'
            return False

    def compare_boards(self):
        if np.allclose(self.prev_board, self.board_to_compare):
            print 'The two boards are the same'
            return False
        else:
            diff_index = np.where(self.prev_board != self.board_to_compare)
            if len(diff_index[0]) == 2:
                color_val_from = self.prev_board[diff_index[0][0]][diff_index[1][0]]
                color_val_to = self.prev_board[diff_index[0][1]][diff_index[1][1]]
                frm =  chr(diff_index[1][0] + 97) +  str(8 - diff_index[0][0])
                to = chr(diff_index[1][1] + 97) + str(8 - diff_index[0][1])
                #If we moved the other way, flip the values
                if color_val_to > 0:
                    (frm, to) = (to, frm)
                return frm + to
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
    c.board_to_compare = board
    if case_number == 1:
        board[1][1] = 0
        board[2][1] = 2
        assert c.check_if_move_is_correct('b7b6')
        assert c.get_move() == 'b7b6', 'Test 1 failed'

    elif case_number == 2:
        board[6][0] = 0
        board[5][0] = 1
        assert c.check_if_move_is_correct('a2a3')
        assert c.get_move() == 'a2a3', 'Test 2 failed'

    elif case_number == 3:
        board[6][0] = 0
        board[1][0] = 1
        assert c.check_if_move_is_correct('a2a7')
        assert c.get_move() == 'a2a7', 'Test 3 failed'

    elif case_number == 4:
        board[1][0] = 0
        board[6][0] = 2
        assert c.check_if_move_is_correct('a7a2')
        assert c.get_move() == 'a7a2', 'Test 4 failed'
if __name__ == '__main__':

    #Test cases:
    #1: Black moves downwards
    #2: White moves upwards
    #3: white captures black
    #4: Black captures white
    #Special cases:
    #5: Promotion
    #6: Castling
    for i in range(1,4):
        test(i)
    print 'All tests passed'
