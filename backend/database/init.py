from sqlmodel import SQLModel, create_engine, Session, delete, select
from sqlalchemy.engine.url import URL

# Must be imported for schema to create in database
from .schema import anime, user, category, tag


connect_url = URL.create(
    drivername="sqlite",
    username="",
    password="",
    host="",
    port=None,
    database="database.db",
    query={}
)
engine = create_engine(connect_url, echo=True)

SQLModel.metadata.create_all(engine)

# with Session(engine) as session:
#     session.exec(delete(User))
#     session.exec(delete(UserSettings))
#     session.exec(delete(Anime))
#     session.exec(delete(Category))
#     session.exec(delete(AnimeCategory))
#     session.commit()

#     me = User(name='reinforce', password='hehe')
#     s = UserSettings(user=me)
#     an = Anime(name='oshi no ko', user=me)
#     session.add(an)
#     session.add(s)
#     session.commit()

#     new_me = session.exec(select(User).where(User.id == 1)).first()
#     new_an = Anime(name='nichijo', user=new_me)
#     session.add(new_an)
#     session.commit()

#     new_an2 = Anime(name='saga', user_id=1)
#     session.add(new_an2)
#     session.commit()

#     ca = Category(name="School", user_id=1)
#     to_add = session.exec(select(Anime).where(Anime.id == 1)).first()
#     to_add.categories.append(ca)
#     session.add(to_add)
#     session.commit()

#     session.refresh(new_an2)
#     session.refresh(ca)
#     new_an2.categories.append(ca)
#     session.add(new_an2)
#     session.commit()