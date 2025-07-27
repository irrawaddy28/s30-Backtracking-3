'''
79 Word Search
https://leetcode.com/problems/word-search/description/

Given an m x n grid of characters board and a string word, return true if word exists in the grid.

The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.


Example 1:
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
Output: true

Example 2:
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "SEE"
Output: true

Example 3:
Input: board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCB"
Output: false


Constraints:
m == board.length
n = board[i].length
1 <= m, n <= 6
1 <= word.length <= 15
board and word consists of only lowercase and uppercase English letters.

Solution:
1. Backtracking using for-loop based recursion:
We scan every cell in the board and check if it contains the first letter of the search word. If it does, we perform a recursion call from every such cell in the grid. Hence, we explore multiple starting cells.

Given the starting cell, we explore adjacent cells (up, down, left, right). If the letter in the adjacent cell matches the next letter in the word, we perform a recursion from the adjacent cell. We mark the adjacent cell as visited (i.e.,in-place mutation, by changing the letter in the cell to lowercase). This helps avoid revisiting the visited cell.

If the adjacent cell doesn't contain the next letter, then we don't visit that cell.

Upon returning from the recursion call, we mark the visited cell as unvisited by uppercasing the letter (getting the cell back to the original board state). This is because, if the path fails, then we give a chance for other paths to explore that cell.

The terminating condition is that anytime we discover the path matches the word, we declare the word exists in the grid and return.

Let W = length of word
Time: At each cell, we have 4 possible choices to recurse. At the max, the recursion depth is just the length of the search word. Hence, 4^W. O(MN) since we explore multiple starting points in the grid.

Time: O(M*N *4^W), Space: O(W), W = length of word

'''
def mprint(matrix):
    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in matrix]))

def exist(board, word):
    def recurse(i, j, wi, path):
        nonlocal found
        if path == word:
            found = True
            return

        for dir in dirs: # for-loop based recursion
            dx, dy = dir[0], dir[1]
            x, y = i+dx, j+dy
            if 0<=x<=M-1 and 0<=y<=N-1:
                if word[wi] == board[x][y]:
                    board[x][y] = board[x][y].lower() # Action
                    recurse(x, y, wi+1, path+word[wi]) # Recursion, O(4^W)
                    if found:
                        return
                    board[x][y] = board[x][y].upper() # Backtrack
        return

    path=""
    found=False
    M = len(board)
    N = len(board[0])
    dirs = [[-1,0],[1,0],[0,-1],[0,1]] # U, D, L, R
    wi=0
    for i in range(M): # O(M)
        for j in range(N): # O(N)
            if word[wi] == board[i][j] and not found:
                board[i][j] = board[i][j].lower() # Action
                recurse(i,j,wi+1,path+word[wi]) # Recursion, O(4^W)
                if found: return found
                board[i][j] = board[i][j].upper() # Backtrack
    return False


def run_exist():
    tests = [([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCCED", True),
             ([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "SEE", True),
             ([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "ABCB", False),
             ([["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "CED", True), # note: we have CES and CED and we are searching for CED. Without backtracking, we could end up marking traversing CE (and changing it to 'ce') and then arrive at the incorrect character S resulting in ceS. We then discard this path and explore a new path from a new starting point. The problem is that this will incorrectly mark 'ce' as visited and limit the traversal for exploring new paths. Only if we use backtracking, we will be to restore 'ce' (visited) to 'CE' (unvisited).
    ]
    for test in tests:
        board, word, ans = test[0], test[1], test[2]
        print(f"\nBoard:")
        mprint(board)
        found = exist(board,word)
        print(f"Search word = {word}")
        print(f"Found = {found}")
        print(f"Path in small letters:")
        mprint(board)
        print(f"Pass: {ans == found}")

run_exist()