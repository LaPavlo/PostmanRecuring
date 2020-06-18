import pytest
from api_engine.api_engine import Books, BaseApi
from helpers.checking_performer import CheckingPerformer, StatusCheck, RequestResponseCompare


@pytest.mark.usefixtures('domain')

class TestClass:
    def test_7_delete_books_duplicates(self):
        books = Books(self.server_url)
        duplicates = books.get_list_of_books_duplicates()
        if len(duplicates) > 0:
            BaseApi.add_simple_step(f'Delete duplicates of books: {duplicates}')
            for id in duplicates:
                status = books.delete_book_and_get_status(str(id))
                BaseApi.add_simple_step(f'Performing tests')
                test_results = CheckingPerformer([
                    StatusCheck(status)
                ]).execute()
                assert test_results == True
            for id in duplicates:
                status, received_response = books.book_status_and_response(str(id))
                test_results = CheckingPerformer([
                    StatusCheck(status, 404)
                ]).execute()
                assert test_results == True
        else:
            BaseApi.add_simple_step(f'No duplicates found')
            assert True
