import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric, Boolean, UniqueConstraint, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()


class User(Base):
	__tablename__='user'
	id=Column(Integer,primary_key=True)
	email=Column(String(80),unique=True,nullable=False)
	name=Column(String(80),nullable=False,unique=True)
	password=Column(String(255),nullable=False)
	#gender=Column(String(8),nullable=False)
	#strAdr=Column(String(255))
	#city=Column(String(10),nullable=False)
	#pincode=Column(Integer,nullable=False)
	#dob=Column(Date)
	#admin=Column(Boolean,default=False)

class Issue(Base):
	__tablename__='issue'
	#On delete left, timezone left, also relztionship pending,current Timestamp pending too,Date time pending too
	id=Column(Integer,primary_key=True)
	author=Column(Integer,ForeignKey('user.id',ondelete="CASCADE"))
	user=relationship(User)
	title=Column(String(80),nullable=False)
	content=Column(String(255),nullable=False)
	lat=Column(Numeric,nullable=False)
	lng=Column(Numeric,nullable=False)
	image=Column(String(250))
	anonFlag=Column(Integer,default=0)
	type=Column(Integer,nullable=0)
	#time=Column(Date)
	#visible=Column(Boolean,default=True)
	like=Column(Integer,default=0)
	dislike=Column(Integer,default=0)


class Comment(Base):
	__tablename__='comment'
	#pending time
	id=Column(Integer,ForeignKey('issue.id',ondelete="CASCADE"))
	issue=relationship(Issue)
	author=Column(Integer,ForeignKey('user.id',ondelete="CASCADE"))
	user=relationship(User)
	content=Column(String(250))
	#time=Column(Date)
	sqNo=Column(Integer,primary_key=True)

class Vote(Base):
	__tablename__='vote'
	#pending: time 
	id=Column(Integer,ForeignKey('issue.id',ondelete="CASCADE"),primary_key=True)
	issue=relationship(Issue)
	author=Column(Integer,ForeignKey('user.id',ondelete="CASCADE"),primary_key=True)
	user=relationship(User)
	like=Column(Integer,default=0)
	dislike=Column(Integer,default=0)
	#time=Column(Date)	

engine=create_engine('sqlite:///IPGS.db')
Base.metadata.create_all(engine)