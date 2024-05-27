from pydantic import BaseModel, Field

class TestModel(BaseModel):
    id: str = Field(alias='id')
    name: str = Field(default='t')
    
class TestModelDB(TestModel):
    id: str = Field(alias='_id')
    
    
model: TestModel = TestModelDB(**{'_id': 'test', 'name': 'test'})
