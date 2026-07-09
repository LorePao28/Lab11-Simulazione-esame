from database.DB_connect import DBConnect
from model.artist import Artist


class DAO():

    @staticmethod
    def getAllGenres():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select * from genre g order by g.Name ASC """

        cursor.execute(query)

        for row in cursor:
            results.append([row["GenreId"], row["Name"]])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(genreId):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct ar.*
                    from artist ar, album al, track t
                    where ar.ArtistId = al.ArtistId and al.AlbumId = t.AlbumId 
                    and t.GenreId = %s """

        cursor.execute(query, (genreId,))

        for row in cursor:
            results.append(Artist(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getPopolarità(idMapArtist, genreId):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select a.ArtistId as a1,  sum(il.Quantity ) as popolarità
                    from album a, track t, invoiceline il, invoice i 
                    where a.AlbumId = t.AlbumId and t.TrackId = il.TrackId and i.InvoiceId = il.InvoiceId and t.GenreId = %s
                    group by a.ArtistId """

        cursor.execute(query, (genreId,))

        for row in cursor:
            if row["a1"] in idMapArtist:
                results.append([idMapArtist[row["a1"]], row["popolarità"]])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getEdges(idMapArtist, genreId):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct t1.a1 as a1, t2.a2 as a2
                    from (select a.ArtistId as a1, i.CustomerId as c1
                    from album a, track t, invoiceline il, invoice i 
                    where a.AlbumId = t.AlbumId and t.TrackId = il.TrackId and i.InvoiceId = il.InvoiceId and t.GenreId = %s
                    group by a.ArtistId, i.CustomerId  ) t1, (select a.ArtistId as a2, i.CustomerId as c2
                    from album a, track t, invoiceline il, invoice i 
                    where a.AlbumId = t.AlbumId and t.TrackId = il.TrackId and i.InvoiceId = il.InvoiceId and t.GenreId = %s
                    group by a.ArtistId, i.CustomerId  ) t2
                    where t1.a1 < t2.a2 and t1.c1 = t2.c2"""

        cursor.execute(query, (genreId, genreId))

        for row in cursor:
            if row["a1"] in idMapArtist and row["a2"] in idMapArtist:
                results.append([idMapArtist[row["a1"]], idMapArtist[row["a2"]]])

        cursor.close()
        conn.close()
        return results

