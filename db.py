from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pymysql
pymysql.install_as_MySQLdb()
engine = create_engine('mysql+pymysql://root:Akanksha%4053@localhost/Hiring_system')
Session = sessionmaker(bind=engine)
session = Session()
