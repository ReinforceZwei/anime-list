from sqlmodel import SQLModel, create_engine, Session, delete, select
from schema.user import User, UserCreate
from schema.category import Category, AnimeCategory
from schema.anime import Anime

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    session.exec(delete(User))
    session.exec(delete(Anime))
    session.exec(delete(Category))
    session.exec(delete(AnimeCategory))
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

    ca = Category(name="School", user_id=1)
    to_add = session.exec(select(Anime).where(Anime.id == 1)).first()
    to_add.categories.append(ca)
    session.add(to_add)
    session.commit()

    session.refresh(new_an2)
    session.refresh(ca)
    new_an2.categories.append(ca)
    session.add(new_an2)
    session.commit()