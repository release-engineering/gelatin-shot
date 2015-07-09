import os
from flask import Flask, url_for, request
from flask_kerberos import requires_authentication, init_kerberos
from sqlalchemy import create_engine, update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, Sequence
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import MetaData, Table
from sqlalchemy.sql.functions import current_timestamp

from ConfigParser import SafeConfigParser

import simplejson as json



Base = declarative_base()
class RHNObject(Base):
    __tablename__ = 'rhnobjects'

    id = Column(Integer, primary_key=True)
    uri = Column(String)

    def __repr__(self):
        return "<RHNObject(id='%s', uri='%s')>" % (self.id, self.uri)

class MD5(Base):
    __tablename__ = 'md5s'

    keyid = Column(Integer, primary_key=True, autoincrement=False)
    hash = Column(String)
    user = Column(String)
    date = Column(DateTime, default=current_timestamp())

    def __repr__(self):
        return "<MD5(keyid='%s', hash='%s', user='%s', date='%s')>" % (self.keyid, self.hash, self.user, self.date)

class SHA256(Base):
    __tablename__ = 'sha256s'

    keyid = Column(Integer, primary_key=True, autoincrement=False)
    hash = Column(String)
    user = Column(String)
    date = Column(DateTime, default=current_timestamp())

    def __repr__(self):
        return "<SHA256(keyid='%s', hash='%s', user='%s', date='%s')>" % (self.keyid, self.hash, self.user, self.date)

parser = SafeConfigParser()
parser.read(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'conf', 'gelatin.conf'))

dbUsername = parser.get("postgresql", "dbusername")
dbPassword = parser.get("postgresql", "dbpass")
dbURL = parser.get("postgresql", "dburl")
engine = create_engine('postgresql://'+dbUsername+':'+dbPassword+'@'+dbURL+'/gelatin', echo=True)

app = Flask(__name__)

init_kerberos(app, hostname='REDHAT.COM')
metadata = MetaData()

Session = sessionmaker()
Session.configure(bind=engine)

def startServer():
    metadata.drop_all(engine)

    rhnobjects = Table('rhnobjects', metadata,
        Column('id', Integer, primary_key=True),
        Column('uri', String(256))
    )
    md5 = Table('md5s', metadata,
        Column('keyid', Integer, primary_key=True, autoincrement=False),
        Column('hash', String(32)),
        Column('user', String(256)),
        Column('date', DateTime, default=current_timestamp())
    )

    sha256 = Table('sha256s', metadata,
        Column('keyid', Integer, primary_key=True, autoincrement=False),
        Column('hash', String(64)),
        Column('user', String(256)),
        Column('date', DateTime, default=current_timestamp())
    )
    metadata.create_all(engine)
#Queries the database for the ID of a URI
#If the URI:ID pair exists in the database, returns the ID
#Otherwise it creates an entry for the URI and gets the generated ID
def getIDFromURI(uri):
    session = Session()

    objectId = session.query(RHNObject, RHNObject.id).filter_by(uri=uri).first()

    if objectId == None:
        newRHNObject = RHNObject(uri = uri)
        session.add(newRHNObject)
        session.commit()
        objectId = session.query(RHNObject, RHNObject.id).filter_by(uri=uri).first().id
    else:
        objectId = objectId.id

    session.close()
    return objectId

@app.route("/api/convert")
def convert():
    pass   

@app.route("/api/retrieve")
def retrieve():
    uris = request.get_json()
    data = {}
    session = Session()
    for uri in uris:
        keyid = getIDFromURI(uri)
        sha256 = session.query(SHA256).filter_by(keyid=keyid).first()
        md5 = session.query(MD5).filter_by(keyid=keyid).first()
        data[uri] = {"sha256": sha256.hash, "md5": md5.hash}
    session.close()
    return json.dumps(data)
    
@app.route("/api/record", methods=['GET', 'POST'])
#@requires_authentication
def record():
    if request.method == 'POST':
        newEntries = request.get_json()
        session = Session()
        for entry in newEntries:
            objectId = getIDFromURI(entry)

            entry = newEntries[entry]

            for checktype in entry:
                checkvalue = entry[checktype]
                tableObjectType = globals()[str(checktype)]
#Todo: Get the user from the kerberos info
                newHashInfo = tableObjectType(keyid = objectId, hash = checkvalue, user = "", date = current_timestamp())
                if session.query(tableObjectType).filter_by(keyid = objectId) == None:
                    session.add(newHashInfo)
                else:
                    session.merge(newHashInfo)
        session.commit()
        session.close()
        return str(newEntries)

if __name__ == "__main__":
    startServer()
    app.run(debug = True)
