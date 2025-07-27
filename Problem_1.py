'''
51 N-Queens
https://leetcode.com/problems/n-queens/description/

The n-queens puzzle is the problem of placing n queens on an n x n chessboard such that no two queens attack each other.

Given an integer n, return all distinct solutions to the n-queens puzzle. You may return the answer in any order.

Each solution contains a distinct board configuration of the n-queens' placement, where 'Q' and '.' both indicate a queen and an empty space, respectively.

Example 1:
Input: n = 4
Output: [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
Explanation: There exist two distinct solutions to the 4-queens puzzle as shown above

Example 2:
Input: n = 1
Output: [["Q"]]


Constraints:
1 <= n <= 9

Solution:
1. For-loop backtracking:
start_row = 0, start_col = 0
Step 0: Place Q in cell(start_row,start_col),
Step 1: Go to next row i = i+1 with j = 0 (col 0)
Step 2: Check if Q can be safely placed in cell (i,j)
        If yes, try next row and go to Step 1 (to find the placement of Q in the next row)
        If no, try next column (j=j+1) and go to Step 2 (to find the placement of Q in the next column)
Step 3: a) If Q cannot be placed in row i, then go back to Step 0, with i = 0, j = 1
        b) If all Qs were placed (one in each row), add it to the result. Go back to Step 0, with start_row = 0, start_col = start_col + 1

One disadvantage with the implementation is that we create and compute the unsafe cells in a new nxn boolean matrix every time we check if it is safe to place Q in a new cell (i,j)

Time to visit all possible solutions = N!
Time to compute visited matrix = N^2
Space = N! calls and for each call we generate a new visited matrix of size N^2
Time: O(N^2 * N!) = O(N^2 * N^N) = O(N^(N+2)), Space: O(N^(N+2))

2. For-loop backtracking without creating a new nxn boolean matrix when we check if the cell is safe or not. We do this by passing the boolean matrix instead of the path by reference. More optimized in terms of memory and time.

Time to visit all possible solutions = N!
Time to compute visited matrix = 4N
Space = O(N^2) since only use the board matrix which acts as the path for backtracking
Time: O(N*N!) = O(N^(N+1)), Space: O(N^2)

3. For-loop backtracking:
This solution is similar to Solution 2 except that:
    a) It starts the recursion from a single starting point (0,0) unlike in solution 2 which starts separately from each column in row 0.
    b) It doesn't need to track the count of how many Qs have been placed so far. Instead it checks if it was able to safely place the Q in the last row and made a recursion call to the last+1 row (non-existent row). If it did, then it means all the N Qs were placed in N rows.
    c) It is easier to understand and more compact.
Time: O(N*N!) = O(N^(N+1)), Space: O(N^2)

https://youtu.be/6ooxRmMGR6Q?t=2588
'''

from copy import deepcopy as dcp
def mprint(matrix):
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))

def solveNQueens_1(n):
    def process_result(n, result):
        L = len(result)
        output = [[None]*n for _ in range(L)]
        for i,res in enumerate(result):
            for row,col in res:
                s = ['.']*n
                s[col] = 'Q'
                s = "".join(s)
                output[i][row] = s
        return output

    def mark_visited_cells(path):
        visited = [[False]*n for _ in range(n)]
        for (i,j) in path:
            # mark columns
            for row in range(n):
                visited[row][j] = True

            # mark rows
            for col in range(n):
                visited[i][col] = True

            # mark diagonals
            dirs = [[-1,-1],[-1,1],[1,-1], [1,1]] # LU, RU, LD, RD
            for dir in dirs:
                p, q = i, j
                while 0<=p<=n-1 and 0<=q<=n-1:
                    x, y = p + dir[0], q + dir[1]
                    if 0<=x<=n-1 and 0<=y<=n-1:
                        visited[x][y] = True
                    p, q = x, y
        return visited

    def is_visited(i,j, path):
        visited = mark_visited_cells(path)
        return visited[i][j]

    def recurse(i, j, count, path):
        if i == n and count == n:
            result.append(path.copy())
            return True

        # place queen in (i,j). go to next row
        success = False
        for j in range(n):
            if not is_visited(i, j, path):
                path.append((i,j))
                success = recurse(i+1, j, count+1, path)
                path.pop()
        return success

    result = []
    for j in range(n):
        path = [(0,j)]
        count = 1
        recurse(1, j, count, path)
        path.pop()
    return process_result(n, result)


def solveNQueens_2(n):
    def mark_cell(board, i, j, c):
        board[i] = board[i][:j] + c + board[i][j+1:]

    def is_visited(i,j, board):
        # check columns
        for row in range(n):
            if board[row][j] == 'Q':
                return True

        # no need to check if row i is safe or not because we are trying to
        # place a Q in row i which is the row next to all occupied rows. In
        # other words,  we know for sure that Q's exist only in the previous rows (0,...,i-1)

        # # check rows
        # for col in range(n):
        #     if board[i][col] == 'Q':
        #         return True

        # check upper diagonals
        dirs = [[-1,-1],[-1,1]] # left upper diag, right upper diag
        for dir in dirs:
            p, q = i, j
            while 0<=p<=n-1 and 0<=q<=n-1:
                x, y = p + dir[0], q + dir[1]
                if 0<=x<=n-1 and 0<=y<=n-1 and board[x][y] == 'Q':
                    return True
                p, q = x, y
        return False

    def recurse(i, count, board):
        if i == n and count == n:
            result.append(board.copy())
            return True

        # place queen in (i,j). go to next row
        success = False
        for j in range(n):
            if not is_visited(i, j, board):
                mark_cell(board,i,j,'Q')
                success = recurse(i+1, count+1, board)
                mark_cell(board,i,j,'.')
        return success

    result = []
    board = ['.'*n for _ in range(n)]
    for j in range(n):
        mark_cell(board,0,j,'Q')
        count = 1
        recurse(1, count, board)
        mark_cell(board,0,j,'.')
    return result

def solveNQueens_3(n):
    def is_safe(i,j):
            # check if column j is safe
            for row in range(n):
                if board[row][j] == 'Q':
                    return False

            # check if left upper diagonal is safe
            row, col = i-1, j-1
            while 0<=row<=n-1 and 0<=col<=n-1:
                if board[row][col] == 'Q':
                    return False
                row -= 1
                col -= 1

            # check if right upper diagonal is safe
            row, col = i-1, j+1
            while 0<=row<=n-1 and 0<=col<=n-1:
                if board[row][col] == 'Q':
                    return False
                row -= 1
                col += 1

            return True

    def recurse(i):
        if i==n:
            result.append(dcp(board))
            return

        for j in range(n):
            if is_safe(i,j):
                board[i][j] = 'Q'
                recurse(i+1)
                board[i][j] = '.'
        return

    board = [['.']*n for _ in range(n)]
    result = []
    recurse(0)
    for r in range(len(result)):
        result[r] = [ "".join(row) for row in result[r]]
    return result

def run_solveNQueens():
    tests = [(1,1), (2,0), (3,0), (4,2), (5,10), (8,92)]
    for test in tests:
        n, ans = test[0], test[1]
        for method in [1,2, 3]:
            if method == 1:
                result=solveNQueens_1(n)
            elif method == 2:
                result=solveNQueens_2(n)
            elif method == 3:
                result=solveNQueens_3(n)
            print(f"\nN={n}")
            print(f"Method {method}: Num of distinct solutions = {len(result)}")
            print(f"Pass: {ans == len(result)}")
            mprint(result)

run_solveNQueens()