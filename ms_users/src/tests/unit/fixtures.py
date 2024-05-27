import pytest


@pytest.fixture()
def correct_emails():
    return [
        'real.email@gmail.com',
        'r.e@g.c',
        'real@gmail.c'
    ]
    

@pytest.fixture()
def wrong_emails():
    return [
        'real.email@gmail.com@',
        'real.emailgmail.com',
        'real email@gmail.com',
        'real@email@gmail.com',
        'real.email@gmail',
        'real.email@',
        '@gmail.com',
        '@',
        'real.email@.',
        'real.email@gm ail.com'
    ]

