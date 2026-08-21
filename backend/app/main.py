from fastapi import FastAPI,Depends
from sqlalchemy import select,func
from sqlalchemy.orm import Session
from .db import Base,engine,get_db
from .models import Event
from .schemas import EventIn,Metrics
app=FastAPI(title='DataPulse Analytics API',version='1.0.0')
Base.metadata.create_all(bind=engine)
@app.get('/health')
def health(): return {'status':'ok'}
@app.post('/events',status_code=201)
def ingest(event:EventIn,db:Session=Depends(get_db)):
 obj=Event(**event.model_dump(exclude_none=True)); db.add(obj); db.commit(); db.refresh(obj); return {'id':obj.id}
@app.get('/analytics/metrics',response_model=Metrics)
def metrics(db:Session=Depends(get_db)):
 return Metrics(events=db.scalar(select(func.count(Event.id))) or 0,users=db.scalar(select(func.count(func.distinct(Event.user_id)))) or 0,sessions=db.scalar(select(func.count(func.distinct(Event.session_id)))) or 0,revenue=float(db.scalar(select(func.coalesce(func.sum(Event.value),0))) or 0))
@app.get('/analytics/top-events')
def top_events(db:Session=Depends(get_db)):
 rows=db.execute(select(Event.event_name,func.count(Event.id).label('count')).group_by(Event.event_name).order_by(func.count(Event.id).desc()).limit(10)).all()
 return [{'event':r.event_name,'count':r.count} for r in rows]
