from sqlalchemy import Table, Column, Integer, String, MetaData,create_engine
meta = MetaData()
engine = create_engine('sqlite:///save_user.db')

UserData = Table(
    'User_Data', meta,
    Column('id', Integer, primary_key=True),
    Column('fb_id', String(10),nullable=False),
    Column('congty', String(100), nullable=False),
    Column('ten', String(100), nullable=False),
    Column('sodienthoai',String(10),nullable=False),
    Column('email', String(50),nullable=False)
)

meta.create_all(engine)