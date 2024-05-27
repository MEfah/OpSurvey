from src.schemas.users import UserResponse, UserUpdate
import pytest
from pydantic import ValidationError


def test_UserReponse():
    correct_user_response = UserResponse(name='name1', description='desc', img_src='img')
    assert correct_user_response.name == 'name1'
    assert correct_user_response.description == 'desc'
    assert correct_user_response.img_src == 'img'
    
    
def test_UserReponse_check_none():
    correct_user_response = UserResponse(name='name1')
    assert correct_user_response.name == 'name1'
    assert correct_user_response.description == None
    assert correct_user_response.img_src == None
    
    
def test_UserReponse_check_required():
    with pytest.raises(ValidationError):
        user_response = UserResponse()
        
        
def test_UserReponse_check_constraints():
    with pytest.raises(ValidationError):
        user_response = UserResponse(name='asdf') # Слишком короткое
        
    with pytest.raises(ValidationError):
        user_response = UserResponse(name='asdf'*20) # Слишком длинное


def test_UserUpdate():
    correct_user_update = UserUpdate(name='name1', description='desc', img_src='img')
    assert correct_user_update.name == 'name1'
    assert correct_user_update.description == 'desc'
    assert correct_user_update.img_src == 'img'
    
    
def test_UserUpdate_check_none():
    correct_user_update = UserUpdate(name='name1')
    assert correct_user_update.name == 'name1'
    assert correct_user_update.description == None
    assert correct_user_update.img_src == None
    
    correct_user_update = UserUpdate(img_src='img')
    assert correct_user_update.name == None
    assert correct_user_update.description == None
    assert correct_user_update.img_src == 'img'
    
    
def test_UserUpdate_check_not_none():
    with pytest.raises(ValidationError):
        user_update = UserUpdate()
        
        
def test_UserUpdate_check_constraints():
    with pytest.raises(ValidationError):
        user_update = UserUpdate(name='asdf') # Слишком короткое
        
    with pytest.raises(ValidationError):
        user_update = UserUpdate(name='asdf'*20) # Слишком длинное