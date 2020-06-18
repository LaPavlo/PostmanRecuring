import pytest
from api_engine.api_engine import Books, BaseApi
from constants.constants import ProjectConstants
from helpers.checking_performer import CheckingPerformer, StatusCheck, SchemaCheck


@pytest.mark.usefixtures('domain')

class TestClass:
    def test_8_json_schema_checking(self, create_book):
        get_books = Books(self.server_url)
        BaseApi.add_simple_step(f'Get books response for {create_book}')
        status, received_response = get_books.book_status_and_response(create_book)
        BaseApi.add_simple_step(f'Performing tests')
        test_results = CheckingPerformer([
            StatusCheck(status),
            SchemaCheck(response_for_schema=received_response,
                        schema=ProjectConstants.SCHEMA)
        ]).execute()
        assert test_results == True