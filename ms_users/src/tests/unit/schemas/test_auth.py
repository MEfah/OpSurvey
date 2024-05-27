from src.schemas.auth import SignUpInfo, SignInInfo
from src.tests.unit.fixtures import wrong_emails, correct_emails
import pytest
from pydantic import ValidationError


def test_SignInInfo():
    correct = SignInInfo(email='real.email@gmail.com', password='normal_password')
    assert correct.email == 'real.email@gmail.com'
    assert correct.password == 'normal_password'
    
    
def test_SignInInfo_validate_required():
    with pytest.raises(ValidationError):
        SignInInfo(password='normal_password')
        
    with pytest.raises(ValidationError):
        SignInInfo(email='real.email@gmail.com')
    
    
def test_SignInInfo_validate_email():
    for email in correct_emails:
        correct = SignInInfo(email=email, password='normal_password')
        assert correct.email == email
        
    for email in wrong_emails:
        with pytest.raises(ValidationError):
            SignInInfo(email=email, password='normal_password')


def test_SignInInfo_validate_password():
    with pytest.raises(ValidationError):
        SignInInfo(email='real.email@gmail.com', password='norm') # Слишком короткий

        
def test_SignUpInfo():
    correct = SignUpInfo(name='normal_name', email='real.email@gmail.com', password='normal_password')
    assert correct.name == 'normal_name'
    assert correct.email == 'real.email@gmail.com'
    assert correct.password == 'normal_password'
    

def test_SignInInfo_validate_required():
    with pytest.raises(ValidationError):
        SignUpInfo(name='normal_name', password='normal_password')
        
    with pytest.raises(ValidationError):
        SignUpInfo(email='real.email@gmail.com')
        
    with pytest.raises(ValidationError):
        SignUpInfo(name='normal_name')
        
    with pytest.raises(ValidationError):
        SignUpInfo(name='normal_name', email='real.email@gmail.com')
    
    
def test_SignUpInfo_validate_name():
    with pytest.raises(ValidationError):
        SignUpInfo(name='norm', email='real.email@gmail.com', password='normal_password') # Слишком короткое
        
    with pytest.raises(ValidationError):
        SignUpInfo(name='norm'*20, email='real.email@gmail.com', password='normal_password') # Слишком длинное
    
    
def test_SignUpInfo_validate_email():
    for email in correct_emails:
        correct = SignUpInfo(name='normal_name', email=email, password='normal_password')
        assert correct.email == email
        
    for email in wrong_emails:
        with pytest.raises(ValidationError):
            SignUpInfo(name='normal_name', email=email, password='normal_password')


def test_SignUpInfo_validate_password():
    with pytest.raises(ValidationError):
        SignUpInfo(name='normal_name', email='real.email@gmail.com', password='norm') # Слишком короткий



