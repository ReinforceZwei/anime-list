from sqlmodel import SQLModel, create_engine, Session, delete, select
from schema.user import User, UserCreate
from schema.anime import Anime

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    session.exec(delete(User))
    session.exec(delete(Anime))
    session.commit()

    me = User(name='reinforce', password='hehe')
    an = Anime(name='oshi no ko', user=me)
    session.add(an)
    session.commit()

    new_me = session.exec(select(User).where(User.id == 1)).first()
    new_an = Anime(name='nichijo', user=new_me)
    session.add(new_an)
    session.commit()

    new_an2 = Anime(name='saga', user_id=1)
    session.add(new_an2)
    session.commit()
