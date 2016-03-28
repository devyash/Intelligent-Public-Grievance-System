from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from DB_setup import Base, Issue, Vote, Comment, User
# Connect to Database and create database session
engine = create_engine('sqlite:///IPGS.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

user1=User(id=1, email="devyashsanghai@gmail.com", name="Devyash", password="ABCD")
session.add(user1)
session.commit()

user2=User(email="abada@gmail.com", name="Abada", password="XYZ")
session.add(user2)
session.commit()

user3=User(email="ka@gmail.com", name="Ka", password="NASND")
session.add(user3)
session.commit()

issue1=Issue(user=user1,title="Big Issue 1",
	content="My problem is BLAH BLAH BLAH BLAH......................................",lat=19.3,
	lng=72.86,
	image="C://images//abx.jpg",
	anonFlag=0, type=1)
session.add(issue1)
session.commit()

issue2=Issue(user=user1,title="Big Issue 2",
	content="HAHAHAHAHAHHAHAHHAHAHAHAAHAHAH",
	lat=20.0,
	lng=72.86,
	image="C://images//abx.jpg",
	anonFlag=0, type=1)
session.add(issue2)
session.commit()

issue3=Issue(user=user1,title="Big Issue 3",
	content="ABCDEFGHIJKLMNOPQRSTUVWXYZ",
	lat=19.3,
	lng=72.86,
	image="C://images//abx.jpg",
	anonFlag=0, type=1)
session.add(issue3)
session.commit()

comment1=Comment(issue=issue3, user=user1, content="Boring Comment 1")
session.add(comment1)
session.commit()

comment2=Comment(issue=issue3, user=user2, content="Boring Comment 2")
session.add(comment2)
session.commit()

comment3=Comment(issue=issue3, user=user1, content="Boring Comment 3")
session.add(comment3)
session.commit()


vote1=Vote( issue=issue1, user=user1, like=1, dislike=0)
session.add(vote1)
session.commit()

print "added DB items!"
