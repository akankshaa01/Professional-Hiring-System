from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:Akanksha%4053@localhost/Hiring_system')
Session = sessionmaker(bind=engine)
session = Session()
