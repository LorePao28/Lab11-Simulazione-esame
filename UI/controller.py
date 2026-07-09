import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceGenre = None

    def fillDDGenre(self):
        lista_genres = self._model.getAllGenres()
        for genre in lista_genres:
            self._view._ddGenre.options.append(ft.dropdown.Option(data= genre,
                                                                  text= genre[1],
                                                                  on_click= self.readDDGenre))
        self._view.update_page()

    def readDDGenre(self, e):
        if e.control.data is None:
            self._choiceGenre = None
        else:
            self._choiceGenre = e.control.data
        print(f"Selezionato il genere {self._choiceGenre}")

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()

        if self._choiceGenre is None:
            self._view.txt_result.controls.append(ft.Text("Selezionare un genere!", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(int(self._choiceGenre[0]))
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato"))
        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {nEdges}"))

        tupla_artista_score = self._model.getInfluenzaArtisti()
        self._view.txt_result.controls.append(ft.Text(f"Artista più influente: {tupla_artista_score[0]}, con influenza: {tupla_artista_score[1]}"))
        self._view.txt_result.controls.append(ft.Text(f"Top 5 archi:"))
        top_five = self._model.getArchiMaggiori()
        for u, v, data in top_five:
            self._view.txt_result.controls.append(ft.Text(f"{u} -> {v}: {data["weight"]}"))
        self._view.update_page()

    def handleCammino(self,e):
        pass