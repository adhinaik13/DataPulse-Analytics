import random
from datetime import datetime,timedelta
from .db import SessionLocal,Base,engine
from .models import Event
Base.metadata.create_all(bind=engine); db=SessionLocal(); now=datetime.utcnow()
for _ in range(10000):
 db.add(Event(event_name=random.choice(['page_view','signup','login','purchase','add_to_cart']),user_id=f'user_{random.randint(1,2500)}',session_id=f'session_{random.randint(1,5000)}',country=random.choice(['India','United Kingdom','United States','Germany','Singapore']),device=random.choice(['desktop','mobile','tablet']),value=round(random.uniform(5,250),2) if random.random()<.12 else 0,occurred_at=now-timedelta(minutes=random.randint(0,43200))))
db.commit(); db.close(); print('Inserted 10,000 demo events')
