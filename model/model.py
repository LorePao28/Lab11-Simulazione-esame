import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._nodes = []
        self._idMapArtist = {}
        self._popolarità = {}

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