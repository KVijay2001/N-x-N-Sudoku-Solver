#SUDOOKU SOLVER BY KISOTHAN

sudoku=[[5,2,'x7',6,1,3],[1,'x7','x7',4,5,2],[2,'x6',1,5,3,4],['x6',4,5,2,6,1],[6,'x6',2,'x6',4,5],['x6','x6',3,1,2,6]]

#Find the missing numbers in each row and return 9 lists with each containing the missing numbers in each row -> absent

all_num=[]
for integer in range(1,len(sudoku)+1):
    all_num.append(integer)

absent=[]
present=[]
for row in sudoku:
    present=[]
    absent_row=[]
    for element in row:
        if type(element)!=str:
            for number in all_num:
                if number==element:
                    present.append(element)
    for number in all_num:
        if number not in present:
            absent_row.append(number)
    absent.append(absent_row)

#Find the possible permutations of absent numbers for each row and remove the permu. with repetitive entries -> all_row_permutations

from itertools import product

all_row_permutations=[]
for row_absent in absent:
    row_combinations=[list(x) for x in list((product(row_absent,repeat=len(row_absent))))]
    comb=row_combinations[:]
    for perm in row_combinations:
        if len(set(perm))!=len(row_absent):
            y=comb.remove(perm)
    all_row_permutations.append(comb)
    
z=all_row_permutations

#Generate all the grid possibilites -> all_possible_grids

c=[z[f] for f in range(len(sudoku))]

i=1
p=c[0]
while i < len(sudoku):
    p=list(product(p,c[i]))
    i+=1

f=0
all_possible_grids=[]
grid=[]
while f < len(p):
    grid.append(p[f][1])
    h=0
    y=p[f][0]
    grid.append(y[1])
    while h < len(sudoku)-2:
        if h!=len(sudoku)-3:
            y=y[0]
            grid.append(y[1])
        else:
            grid.append(y[0])
        h+=1
    grid.reverse()
    all_possible_grids.append(grid)
    grid=[]
    f+=1

# Replace the missing values by the expected possibilities and produce all the possible complete sudoku grids -> all_candidates

all_candidates=[]

i=0
j=0

def slotting(possible_grid):
    """_"""
    candidate=[]
    sudoku=[[5,2,'x7',6,1,3],[1,'x7','x7',4,5,2],[2,'x6',1,5,3,4],['x6',4,5,2,6,1],[6,'x6',2,'x6',4,5],['x6','x6',3,1,2,6]]
    candidate=sudoku[:]
    i=0
    for row_entries in possible_grid:
        k=0
        for entry in sudoku[i]:
            if type(entry)==str:
                candidate[i][sudoku[i].index(entry)]=row_entries[k]
                k+=1
        i+=1
    return(candidate)

for possible_grid in all_possible_grids:
    all_candidates.append(slotting(possible_grid))


# EVALUATION 1 : Collect the columns of each possible sudoku grid and see if the entries in the columns form a set of N. If not, remove them from the selected list. -> all_candidates = all sudoku grids that have passed evaluation 1 

all_candidates_columns=[]
for candidate_sudoku in all_candidates:
    columns=[]
    for u in range(len(sudoku)):
        vertical=[]
        for row in candidate_sudoku:
            vertical.append(row[u])
        columns.append(vertical)
    all_candidates_columns.append(columns)

removed=[]
for candidate_columns in all_candidates_columns:
    for column in candidate_columns:
        if len(set(column))!=len(sudoku) and candidate_columns not in removed:
            removed.append(candidate_columns)

index=[]
for bad_candidate_columns in removed:
    index.append(all_candidates_columns.index(bad_candidate_columns))

bad_candidates=[]
for ind in index:
    bad_candidates.append(all_candidates[ind])
for bad_candidate in bad_candidates:
    all_candidates.remove(bad_candidate)

# EVALUATION 2 : Identify the different squares/rectangles in each possible sudoku grid, verify that the entries in those boxes form a set of N and if not remove them from final list. -> all_candidates = remaining unique solution

from math import sqrt

n=len(sudoku)
root=sqrt(n)

if int(root+0.5)**2==n:
    track=[]
    list_of_tracks=[]

    l=0
    row1=[]
    for k in range(int(root)):
        row1.append(l)
        l+=int(root)

    e=0
    column1=[]
    for w in range(int(root)):
        column1.append(e)
        e+=int(root)

if n%2==0:
    a=2
    b=int(n/2)
   
    l=0
    row2=[]
    for k in range(b):
        row2.append(l)
        l+=2

    e=0
    column2=[]
    for w in range(2):
        column2.append(e)
        e+=b
    
    
candidates_tracks=[]
track=[]
list_of_tracks=[]
for candidate in all_candidates:
    if int(root+0.5)**2==n:
        for g in row1:
            old_g=g
            for f in column1:
                old=f
                p=0
                g=old_g
                while p < root:
                    f=old
                    b=0
                    while b < root:
                       track.append(candidate[g][f])
                       f+=1
                       b+=1
                    g+=1
                    p+=1
                list_of_tracks.append(track)
                track=[]
    elif n%2==0:
        a=2
        b=int(n/2)
        m=0
        for g in row2:
            old_g=g
            for f in column2:
                old=f
                p=0
                g=old_g
                while p < 2:
                    f=old
                    d=0
                    while d < b:
                        track.append(candidate[g][f])
                        f+=1
                        d+=1
                    g+=1
                    p+=1
                list_of_tracks.append(track)
                track=[]
    else:
        print('Invalid Sudoku Format. Pls enter a n x n list of lists where n is an even number superior to 3.' )
    candidates_tracks.append(list_of_tracks)
    
remove=[]
for candidate in candidates_tracks:
    for track in candidate:
        if len(set(track))!=len(sudoku):
            remove.append(candidates_tracks.index(candidate))
elim=[]
for index in remove:
    elim.append(all_candidates[index])

for bad in elim:
    all_candidates.remove(bad)

print(all_candidates[0])