import json
from api_engine.api_engine import Books, BaseApi
from random import randint, random


import pytest
import requests
from faker import Factory
from constants.constants import ProjectConstants

def pytest_addoption(parser):
    parser.addoption("--server", action="store", help="server that you wanna test against")

@pytest.fixture(scope="session")
def server(request):
    return request.config.getoption("--server")

@pytest.fixture(scope="class")
def domain(request, server):
    if server == ProjectConstants.LOCAL:
        server_url = ProjectConstants.LOCAL_SERVER_URL
    else:
        server_url = server
    if request.cls is not None:
        request.cls.server_url = server_url
    return server_url

@pytest.fixture(scope= "class")
def book_id(domain):
    book_id = str(randint(200, 999))
    fake = Factory.create()
    title = fake.catch_phrase()
    author = fake.name()
    rating = fake.year()
    year_published = fake.year()
    data = {
        "id": book_id,
        "title": title,
        "author": author,
        "rating": rating,
        "year_published": year_published
    }
    requests.post(ProjectConstants.LOCAL_SERVER_URL +  ProjectConstants.BOOKS_ENDPOINT, data)
    return book_id

@pytest.fixture(scope= "class")
def book_id_list(domain):
    book_id_list_fixture = BaseApi(domain)
    status, response_items = book_id_list_fixture.get_status_and_response(ProjectConstants.BOOKS_ENDPOINT)
    list_of_founded_ids = []
    for dic in response_items:
        if dic.get("author") == ProjectConstants.TITLE_TO_FIND:
            list_of_founded_ids.append(dic.get("id"))
    return list_of_founded_ids

@pytest.fixture(scope= "class")
def create_book(domain):
    fake = Factory.create()
    title = fake.catch_phrase()
    author = fake.name()
    rating = fake.year()
    year_published = fake.year()
    data = {
        "title" : title,
        "author" : author,
        "rating" : rating,
        "year_published" : year_published
    }
    create_book_fixture = BaseApi(domain)
    status, response_items = create_book_fixture.post_and_get_status_and_response(ProjectConstants.BOOKS_ENDPOINT, data)
    id = response_items.get("id")
    return id


