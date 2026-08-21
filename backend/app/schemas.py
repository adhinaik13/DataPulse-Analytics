from datetime import datetime
from pydantic import BaseModel
class EventIn(BaseModel):
 event_name:str; user_id:str; session_id:str; country:str='Unknown'; device:str='desktop'; value:float=0; occurred_at:datetime|None=None
class Metrics(BaseModel):
 events:int; users:int; sessions:int; revenue:float
