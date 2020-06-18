class ProjectConstants:
    LOCAL = "local"
    LOCAL_SERVER_URL = "http://localhost:3000"
    BOOKS_ENDPOINT = "books"
    SHOPS_ENDPOINT = "shops"
    BOOK_ID = "/101"
    SHOPS_DEFAULT_AMOUNT = 20
    LOGIN = "mobidev"
    PASSWORD = "Temp@123"
    EXPECTED_RESPONSE = {"id":101,"title":"nemo labore","author":"Lorenz Schneider","rating":1.55,"year_published":1766}
    DEFAULT_TEST_NAME_FOR_COMPARE_RESPONSE = 'Compare actual response with expected'
    TITLE_TO_FIND = "Bradly Frami"
    SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "default": {},
    "examples": [
        {
            "title": "Enhanced grid-enabled concept",
            "author": "Tammy Torres",
            "rating": "1970",
            "year_published": "1987",
            "id": "zysjYlg"
        }
    ],
    "required": [
        "title",
        "author",
        "rating",
        "year_published",
        "id"
    ],
    "additionalProperties": True,
    "properties": {
        "title": {
            "$id": "#/properties/title",
            "type": "string",
            "title": "The title schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "Enhanced grid-enabled concept"
            ]
        },
        "author": {
            "$id": "#/properties/author",
            "type": "string",
            "title": "The author schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "Tammy Torres"
            ]
        },
        "rating": {
            "$id": "#/properties/rating",
            "type": "string",
            "title": "The rating schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "1970"
            ]
        },
        "year_published": {
            "$id": "#/properties/year_published",
            "type": "string",
            "title": "The year_published schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "1987"
            ]
        },
        "id": {
            "$id": "#/properties/id",
            "type": "string",
            "title": "The id schema",
            "description": "An explanation about the purpose of this instance.",
            "default": "",
            "examples": [
                "zysjYlg"
            ]
        }
    }
}