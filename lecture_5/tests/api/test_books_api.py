from tests.mocks.factories import BookInSchemaFactory


class TestBooksAPI:
    def test_create_book(self, client):
        book_data = BookInSchemaFactory.build().model_dump()
        response = client.post("/books/", json=book_data)

        assert response.status_code == 201
        data = response.json()["data"]
        assert data["title"] == book_data["title"]
        assert data["author"] == book_data["author"]
        assert data["year"] == book_data["year"]
        assert "id" in data

    def test_get_all_books(self, client):
        book_data = BookInSchemaFactory.build().model_dump()
        client.post("/books/", json=book_data)

        response = client.get("/books/")

        assert response.status_code == 200
        data = response.json()["data"]
        assert "items" in data
        assert "pagination" in data

    def test_get_book_by_id(self, client):
        book_data = BookInSchemaFactory.build().model_dump()
        create_response = client.post("/books/", json=book_data)
        book_id = create_response.json()["data"]["id"]

        response = client.get(f"/books/{book_id}")

        assert response.status_code == 200
        data = response.json()["data"]
        assert data["id"] == book_id

    def test_get_book_not_found(self, client):
        response = client.get("/books/99999")

        assert response.status_code == 404

    def test_update_book(self, client):
        book_data = BookInSchemaFactory.build().model_dump()
        create_response = client.post("/books/", json=book_data)
        book_id = create_response.json()["data"]["id"]

        new_title = BookInSchemaFactory.build().title
        response = client.put(f"/books/{book_id}", json={"title": new_title})

        assert response.status_code == 200
        data = response.json()["data"]
        assert data["title"] == new_title

    def test_update_book_not_found(self, client):
        response = client.put("/books/99999", json={"title": "New"})

        assert response.status_code == 404

    def test_delete_book(self, client):
        book_data = BookInSchemaFactory.build().model_dump()
        create_response = client.post("/books/", json=book_data)
        book_id = create_response.json()["data"]["id"]

        response = client.delete(f"/books/{book_id}")

        assert response.status_code == 200

        get_response = client.get(f"/books/{book_id}")
        assert get_response.status_code == 404

    def test_delete_book_not_found(self, client):
        response = client.delete("/books/99999")

        assert response.status_code == 404

    def test_search_books_by_title(self, client):
        book_data = BookInSchemaFactory.build().model_dump()
        client.post("/books/", json=book_data)

        search_term = book_data["title"][:5]
        response = client.get("/books/search/", params={"title": search_term})

        assert response.status_code == 200
        data = response.json()["data"]
        assert "items" in data

    def test_search_books_by_author(self, client):
        book_data = BookInSchemaFactory.build().model_dump()
        client.post("/books/", json=book_data)

        response = client.get("/books/search/", params={"author": book_data["author"]})

        assert response.status_code == 200

    def test_pagination(self, client):
        for _ in range(5):
            book_data = BookInSchemaFactory.build().model_dump()
            client.post("/books/", json=book_data)

        response = client.get("/books/", params={"page": 0, "limit": 2})

        assert response.status_code == 200
        data = response.json()["data"]
        assert len(data["items"]) <= 2
        assert data["pagination"]["limit"] == 2
