"""

@author Kiettiphong Manovisut

References:
https://en.wikipedia.org/wiki/Word_error_rate
https://www.github.com/mission-peace/interview/wiki

"""
import numpy

def get_word_error_rate(r, h):
    print("r :",r,"\nh :",h)
    """
    Given two list of strings how many word error rate(insert, delete or substitution).
    """
    d = numpy.zeros((len(r) + 1) * (len(h) + 1), dtype=numpy.uint16)
    d = d.reshape((len(r) + 1, len(h) + 1))
    for i in range(len(r) + 1):
        for j in range(len(h) + 1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i

    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitution = d[i - 1][j - 1] + 1
                insertion = d[i][j - 1] + 1
                deletion = d[i - 1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)
    result = float(d[len(r)][len(h)]) / len(r) * 100
    print("First result :",result)
    x = len(r)
    y = len(h)
    substitution = 0
    deletion = 0
    insertion = 0
    correct =0
    while True:
        if x == 0 or y == 0:
            break
        if r[x - 1] == h[y - 1]:
            x = x - 1
            y = y - 1
            correct += 1
        elif d[x][y] == d[x - 1][y - 1] + 1:    # substitution
            x = x - 1
            y = y - 1
            substitution+=1
        elif d[x][y] == d[x - 1][y] + 1:        # deletion
            x = x - 1
            deletion += 1
        elif d[x][y] == d[x][y - 1] + 1:        # insertion
            y = y - 1
            insertion += 1
        else:
            print('\nWe got an error.')
            break
    print(">>>",substitution,deletion,insertion,correct)
    print(float((substitution+deletion+insertion)/len(r)))
    print(float((substitution+deletion+insertion)/(substitution+deletion+correct)))
    return (substitution,deletion,insertion)

  

if __name__ == "__main__":
    r = "เราไปทำงานที่นี่น้า"
    h = "เรไปทำงานที่นี่น้ะ"
    print(get_word_error_rate(r,h))