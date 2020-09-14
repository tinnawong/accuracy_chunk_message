"""

@author Kiettiphong Manovisut

References:
https://en.wikipedia.org/wiki/Word_error_rate
https://www.github.com/mission-peace/interview/wiki

"""
import numpy


def get_word_error_rate(r, h):
    """
    Given two list of strings how many word error rate(insert, delete or substitution).
    """

    dimensions = numpy.zeros((len(r) + 1) * (len(h) + 1), dtype=numpy.uint16)
   
    dimensions = dimensions.reshape((len(r) + 1, len(h) + 1))
    for i in range(len(r) + 1):
        for j in range(len(h) + 1):
            if i == 0:
                dimensions[0][j] = j
            elif j == 0:
                dimensions[i][0] = i
    print(dimensions)
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                dimensions[i][j] = dimensions[i - 1][j - 1]
                print(i,j ,">>>",i-1,j-1)
            else:
                #1 2
                substitution = dimensions[i - 1][j - 1] + 1
                insertion = dimensions[i][j - 1] + 1
                deletion = dimensions[i - 1][j] + 1
                print(i,j,"=",substitution,insertion,deletion)
                dimensions[i][j] = min(substitution, insertion, deletion)
    result = float(dimensions[len(r)][len(h)]) / len(r) * 100
    print("type : ",type(dimensions[0][0]))
    print("dimensions id ",id(dimensions))

    print_to_html(r, h,dimensions)
    return result


def print_to_html(r, h, dimensions):
    print("dimensions id ",id(dimensions))
    print(id(r))
    x = len(r)
    y = len(h)
    
    while True:
        if x == 0 or y == 0:
            break
        print(r[x - 1] ," vs ", h[y - 1]," = ",x,y)
        if r[x - 1] == h[y - 1]:
            x = x - 1
            y = y - 1
            # html = '%s ' % h[y] + html
        elif dimensions[x][y] == dimensions[x - 1][y - 1] + 1:    # substitution
            x = x - 1
            y = y - 1
            # html = '<span class="y">%s(%s)</span> ' % (h[y], r[x]) + html

            
        elif dimensions[x][y] == dimensions[x - 1][y] + 1:        # deletion
            x = x - 1
            # html = '<span class="r">%s</span> ' % r[x] + html
        elif dimensions[x][y] == dimensions[x][y - 1] + 1:        # insertion
            y = y - 1
            # html = '<span class="g">%s</span> ' % h[y] + html
        else:
            print('\nWe got an error.')
            break


if __name__ == "__main__":
    wordFull = "เรามาทำงานที่นี่"
    r = "เรามา"
    h = "เรามาส"
    print(id(r))
    print(get_word_error_rate(r,h))