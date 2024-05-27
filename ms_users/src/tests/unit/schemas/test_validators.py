from src.schemas.validators import is_email
from src.tests.unit.fixtures import wrong_emails, correct_emails


def test_is_email(wrong_emails, correct_emails):
    for email in correct_emails:
        assert is_email(email)
        
    for email in wrong_emails:
        assert not is_email(email)