from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, create_engine, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    character_name = Column(String, nullable=False)
    auditions = relationship("Audition", back_populates="role")

    def actors(self):
        return [audition.actor for audition in self.auditions]

    def locations(self):
        return [audition.location for audition in self.auditions]

    def lead(self):
        hired_auditions = [a for a in self.auditions if a.hired]
        return hired_auditions[0] if hired_auditions else "no actor has been hired for this role"

    def understudy(self):
        hired_auditions = [a for a in self.auditions if a.hired]
        return hired_auditions[1] if len(hired_auditions) > 1 else "no actor has been hired for understudy for this role"
    

class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer, primary_key=True)
    actor = Column(String, nullable=False)
    location = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    hired = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship("Role", back_populates="auditions")

    def call_back(self):
        self.hired = True

engine = create_engine("sqlite:///auditions.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()





# Create some roles
Lucifer_Morningstar = Role(character_name="Lucifer_Morningstar")
Chloe_Decker = Role(character_name="Chloe_Decker")

# Add to session
session.add_all([Lucifer_Morningstar, Chloe_Decker])
session.commit()

# Create auditions and assign roles
audition1 = Audition(actor="Pascal Tokodi ", location="Nairobi", phone=254+712345678, role=Lucifer_Morningstar)
audition2 = Audition(actor="Nick Mutuma", location="Naivasha", phone=254+702345678, role=Lucifer_Morningstar)
audition3 = Audition(actor="Sarah Hassan", location="Nairobi", phone=254+700345678, role=Chloe_Decker)
audition4 = Audition(actor="Brenda Wairimu", location="Nairobi", phone=254+700045678, role=Chloe_Decker)

# Add auditions
session.add_all([audition1, audition2, audition3, audition4])
session.commit()

audition1.call_back()
audition3.call_back()
session.commit()
