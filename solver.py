import sys
from collections import deque
from time import sleep

#+-+---+--------+
#|X|     |     -|
#| | --+ | +--  |
#| |   | | |    |
#| +-- | | |  --+
#|     |   |   #|
#+-----+---+----+
#
#
#  Rules:
#  Always turn left if you can
#  If you cannot turn left, go straight
#  If you cannot turn left or go straight, turn right
#  If you cannot turn left, go straight, or turn right, turn around because 
#  youmust be at a dead end.

if len(sys.argv)!=2:
    print "* Usage: python {} mazefile.txt".format(__file__)
    exit()

# Assume maze dimensions are fine, and file only contents a maze
def load_maze(fname):
    return list(file(fname,'rb').read().replace('\n',''))

def search_pj(maze,pj='X'):
    for i in range(len(maze)):
        if maze[i]==pj:
            return i
    return -1

def is_wall(some):
    return some in ['+', '|', '-']

def can_turn_left(maze, pos, facing):
    if facing[0]=='N' and not is_wall(maze[pos-1]): #param dim
        return True
    elif facing[0]=='W' and not is_wall(maze[pos+16]): #param dim
        return True 
    elif facing[0]=='S' and not is_wall(maze[pos+1]): #param dim
        return True
    elif facing[0]=='E' and not is_wall(maze[pos-16]): #param dim
        return True
    else:
        return False

def can_forward(maze, pos, facing):
    return  ( facing[0]=='N' and not is_wall(maze[pos-16]) ) or \
            ( facing[0]=='W' and not is_wall(maze[pos-1]) ) or \
            ( facing[0]=='S' and not is_wall(maze[pos+16]) ) or \
            ( facing[0]=='E' and not is_wall(maze[pos+1]) )  

def can_turn_right(maze, pos, facing):
    return  ( facing[0]=='N' and not is_wall(maze[pos+1]) ) or \
            ( facing[0]=='W' and not is_wall(maze[pos-16]) ) or \
            ( facing[0]=='S' and not is_wall(maze[pos-1]) ) or \
            ( facing[0]=='E' and not is_wall(maze[pos+0x10]) )  

def step(maze, pos, facing):
    current = pos
    if facing[0] == 'N':
        new_pos = pos-16
    elif facing[0] == 'W':
        new_pos = pos-1
    elif facing[0] == 'S':
        new_pos = pos+16
    else:
        new_pos = pos+1
    maze[pos]=' '
    maze[new_pos]='X'
    return new_pos

def win(maze,pos):
    return (maze[pos-1]=='#') or \
            (maze[pos+1]=='#') or \
            (maze[pos-16]=='#') or \
            (maze[pos+16]=='#') 

def print_maze(maze):
    for i in range(0,len(maze),16):
        print ''.join(maze[i:i+16])

def solve(maze, start, prize='#'):
    facing = deque(['N', 'W', 'S', 'E'])
    pos = start

    while not win(maze,pos):
        if can_turn_left(maze,pos,facing):
            facing.rotate(-1)    
        elif can_forward(maze,pos,facing):
            pass
        elif can_turn_right(maze,pos,facing):
            facing.rotate(1)    
        else:
            facing.rotate(2)
        pos=step(maze,pos,facing)
        print "@@@@@@@@@@@@@@@@@@"
        print_maze(maze)
        sleep(1)
    print "WIN!"

if __name__ == '__main__':
    fname=sys.argv[1]
    maze=load_maze(fname)
    print_maze(maze)
    start=search_pj(maze)
    solve(maze,start)
