import matplotlib.pyplot as plt
import matplotlib.cm
import matplotlib.colors

def visualisation(vertices):
    min_col, min_row, max_col, max_row = 0, 0, 0, 0
    for vertice in vertices:
        min_col = min(vertice[1], min_col)
        max_col = max(vertice[1], max_col)
        min_row = min(vertice[0], min_row)
        max_row = max(vertice[0], max_row)
    fig, axes = plt.subplots(1, 1)
    row, col = [], []
    for i in range(len(vertices)):
        row.append(vertices[i][0] + abs(min_row))
        col.append(vertices[i][1] + abs(min_col))
    row.append(vertices[0][0] + abs(min_row))
    col.append(vertices[0][1] + abs(min_col))
    plt.plot(row, col, color="green")
    plt.show()
