class Solution:

    def issafe(self, vertex, col, adj, color):
        for it in adj[vertex]:
            if color[it] != -1 and col == color[it]:
                return False
        return True

    def solve(self, vertex, m, adj, color):
        if vertex == len(color):
            return True

        for i in range(m):
            if self.issafe(vertex, i, adj, color):
                color[vertex] = i

                if self.solve(vertex + 1, m, adj, color):
                    return True

                color[vertex] = -1

        return False

    def graphColoring(self, v, edges, m):
        adj = [[] for _ in range(v)]

        for u, w in edges:
            adj[u].append(w)
            adj[w].append(u)

        color = [-1] * v

        result = self.solve(0, m, adj, color)

        if result:
            print("Color Assignment:", color)

        return result


def main():
    v = 4
    edges = [
        [0, 1],
        [1, 2],
        [2, 3],
        [3, 0]
    ]
    m = 2

    obj = Solution()

    if obj.graphColoring(v, edges, m):
        print("Graph can be colored with", m, "colors.")
    else:
        print("Graph cannot be colored with", m, "colors.")


if __name__ == "__main__":
    main()