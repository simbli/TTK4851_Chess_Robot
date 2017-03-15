import cv2
import numpy as np
from ip import getRepresentation, calibrate
#from video import get_frame
import sys

def get_frame():
    return cv2.imread(sys.argv[1],1)

def createInitialBoardMatrix():
        initialBoard = np.zeros((8,8))
        initialBoard[:2][:] = 2
        initialBoard[6:][:] = 1
        return initialBoard

#Class for getting move
class Compvision():
    #Initialize with image of first board
    def __init__(self):

        self.boundaries = calibrate()
        print 'Calibration is complete, please put chesspieces to their positions'

        initialBoard = createInitialBoardMatrix()
        currentBoard = getRepresentation(self.boundaries, get_frame())
        while not np.array_equal(initialBoard, currentBoard):
            print 'Could not detect correct setup, try again'
            currentBoard = getRepresentation(self.boundaries, get_frame())
        self.prev_board = currentBoard
        self.board_to_compare = None
    #Takes a new snapshot, and compares the previous one with the new, gives out a move

    def get_move(self):
        self.board_to_compare = getRepresentation(self.boundaries, get_frame())
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
                color_val_from = self.board_to_compare[diff_index[0][0]][diff_index[1][0]]
                color_val_to = self.board_to_compare[diff_index[0][1]][diff_index[1][1]]
                frm =  chr(diff_index[1][0] + 97) +  str(8 - diff_index[0][0])
                to = chr(diff_index[1][1] + 97) + str(8 - diff_index[0][1])
                #If we moved the other way, flip the values
                if color_val_to == 0:
                    (frm, to) = (to, frm)
                return frm + to
            elif len(diff_index[0]) == 4:
                if all(self.prev_board[7][4:] == [1,0,0,1]):
                    return 'e1g1'
                elif all(self.prev_board[7][:5] == [1,0,0,0,1]):
                    return 'e1c1'
                elif all(self.prev_board[0][4:] == [2,0,0,2]):
                    return 'e8g8'
                elif all(self.prev_board[0][:5] == [2,0,0,0,2]):
                    return 'e8c8'
                else:
                    print 'an error occured'

            else:
                print len(diff_index[0])
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
        c.prev_board[1][1] = 0
        c.board_to_compare[2][1] = 2
        assert c.check_if_move_is_correct('b7b6')
        assert c.get_move() == 'b7b6', 'Test 1 failed'

    elif case_number == 2:
        c.board_to_compare[6][0] = 0
        c.board_to_compare[5][0] = 1

        assert c.check_if_move_is_correct('a2a3')
        assert c.get_move() == 'a2a3', 'Test 2 failed'

    elif case_number == 3:
        c.board_to_compare[6][0] = 0
        c.board_to_compare[1][0] = 1
        assert c.check_if_move_is_correct('a2a7')
        assert c.get_move() == 'a2a7', 'Test 3 failed'

    elif case_number == 4:
        c.board_to_compare[1][0] = 0
        c.board_to_compare[6][0] = 2
        assert c.check_if_move_is_correct('a7a2')
        assert c.get_move() == 'a7a2', 'Test 4 failed'

    elif case_number == 5:
        c.prev_board[7] = [1,0,0,0,1,1,1,1]
        c.board_to_compare[7] = [0,0,1,1,0,1,1,1]
        print c.prev_board
        print '\n'
        print c.board_to_compare
        assert c.check_if_move_is_correct('e1c1')
        assert c.get_move() == 'e1c1', 'Test 4 failed'

    elif case_number == 6:
        c.prev_board[7] = [1,1,1,1,1,0,0,1]
        c.board_to_compare[7] = [1,1,1,1,0,1,1,0]
        print c.prev_board
        print c.board_to_compare
        assert c.check_if_move_is_correct('e1g1')
        assert c.get_move() == 'e1g1', 'Test 4 failed'

    elif case_number == 7:
        c.prev_board[0] = [2,0,0,0,2,2,2,2]
        c.board_to_compare[0] = [0,0,2,2,0,2,2,2]
        assert c.check_if_move_is_correct('e8c8')
        assert c.get_move() == 'e8c8', 'Test 4 failed'

    elif case_number == 8:
        c.prev_board[0] = [2,2,2,2,2,0,0,2]
        c.board_to_compare[0] = [2,2,2,2,0,2,2,0]
        assert c.check_if_move_is_correct('e8g8')
        assert c.get_move() == 'e8g8', 'Test 4 failed'

if __name__ == '__main__':

    #Test cases:
    #1: Black moves downwards
    #2: White moves upwards
    #3: white captures black
    #4: Black captures white
    #Special cases:
    #6: Promotion
    #Castling white
        #5: Castling queens side
        #6: Castling kings side
    #7: Castling black
        #7: Castling queens side
        #8: Castling kings side
    for i in range(1,8):
        test(i)
    print 'All tests passed'

    c = Compvision()
