import pytest
from api_engine.api_engine import Books, BaseApi
from helpers.checking_performer import CheckingPerformer, StatusCheck, RequestResponseCompare

@pytest.mark.usefixtures('domain')

class TestClass:
    def test_5_create_book(self):
        post_book = Books(self.server_url)
        BaseApi.add_simple_step(f'Generate request body for {post_book.books_endpoint}')
        book_to_post = post_book.create_book_data()
        BaseApi.add_simple_step(f'Post book to endpoint: {post_book.books_endpoint}')
        status, received_response = post_book.post_new_book(book_to_post)
        BaseApi.add_simple_step(f'Performing tests')
        test_results = CheckingPerformer([
            StatusCheck(status, 201),
            RequestResponseCompare([[received_response, book_to_post]])
        ]).execute()
        assert test_results == True