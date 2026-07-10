import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._nodes = []
        self._idMapArtist = {}
        self._popolarità = {}
        self._optPath = []
        self._optLenght = 0

    def getAllGenres(self):
        return DAO.getAllGenres()

    def buildGraph(self, genreId):
        print("Creo grafo")
        self._graph.clear()
        self._idMapArtist.clear()
        self._nodes = DAO.getAllNodes(genreId)
        for n in self._nodes:
            self._idMapArtist[n.ArtistId] = n
        self._graph.add_nodes_from(self._nodes)
        self.setPopolarità(genreId)
        self.addEdges(genreId)

    def setPopolarità(self, genreId):
        lista_result = DAO.getPopolarità(self._idMapArtist, genreId)
        for row in lista_result:
            self._popolarità[row[0]] = int(row[1])

    def addEdges(self, genreId):
        lista_artist = DAO.getEdges(self._idMapArtist, genreId)
        for row in lista_artist:
            peso = self._popolarità[row[0]] + self._popolarità[row[1]]
            if self._popolarità[row[0]] > self._popolarità[row[1]]:
                self._graph.add_edge(row[0], row[1], weight=peso)
            elif self._popolarità[row[0]] < self._popolarità[row[1]]:
                self._graph.add_edge(row[1], row[0], weight=peso)
            elif self._popolarità[row[0]] == self._popolarità[row[1]]:
                self._graph.add_edge(row[0], row[1], weight=peso)
                self._graph.add_edge(row[1], row[0], weight=peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getInfluenzaArtisti(self):
        listNodesPesata = []
        for n in self._graph.nodes:
            score = 0
            for e in self._graph.out_edges(n, data=True):
                score += e[2]["weight"]
            for e in self._graph.in_edges(n, data=True):
                score -= e[2]["weight"]
            listNodesPesata.append((n, score))

        listNodesPesata.sort(key=lambda x: x[1], reverse=True)

        return listNodesPesata[0]

    def getArchiMaggiori(self):
        listNodesPesata = sorted(self._graph.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)

        return listNodesPesata[0:5]


    def findPath(self, a):
        self._optPath = []
        self._optLenght = 0

        parziale = [a]
        for n in self._graph.out_edges(a, data=True):
            parziale.append(n)
            self._ricorsione(parziale)
            parziale.pop()
        return self._optPath, self._optLenght

    def _ricorsione(self, parziale):
        if len(list(self._graph.out_edges(parziale[-1]))) == 0:
            if len(parziale) > self._optLenght:
                self._optLenght = len(parziale)
                self._optPath = copy.deepcopy(parziale)
            return
        else:
            for n in self._graph.out_edges(parziale[-1]):
                if self._graph[parziale[-1]][n]["weight"] > self._graph[parziale[-2]][parziale[-1]]["weight"] and n not in parziale:
                    parziale.append(n)
                    self._ricorsione(parziale)
                    parziale.pop()

    def getBestPath2(self, source):

        self._bestPath = []

        partial = [self._idMap[int(source)]]

        for _, v, data in self._graph.out_edges(self._idMap[int(source)], data=True):
            partial.append(v)

            self._ricorsione(partial, data["weight"])
            partial.pop()

        return self._bestPath

    def _ricorsione2(self, partial, lastWeight):

        # update best solution
        if len(partial) > len(self._bestPath):
            self._bestPath = copy.deepcopy(partial)

        current = partial[-1]

        for _, successor, data in self._graph.out_edges(current, data=True):

            weight = data["weight"]

            # strictly decreasing weights
            if weight > lastWeight:

                # simple path
                if successor not in partial:
                    partial.append(successor)

                    self._ricorsione(partial, weight)

                    partial.pop()