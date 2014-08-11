#from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa
Base = declarative_base()

class Foo(Base):
    __tablename__ = 'foo'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50))


def generate_variable_table_class_type(name):
    """This is a helper function which dynamically creates a new ORM enabled class
    The table will hold the individual values of each variable
    Individual values are stored as a string
    """
    def __init__(self,value):
        self.value = str(value)
        
    def __str__(self):
        return self.value
    
    def __repr__(self):
        return self.value     
          
    attr_dict =  {
                  '__tablename__' : "vector_{}".format(name),
                  'id' : sa.Column(sa.Integer, primary_key=True),
                  'value' : sa.Column(sa.String(16), nullable=False, unique=True),
                  '__init__' : __init__,
                  '__str__' : __str__,
                  '__repr__' : __repr__,
                  }
        
    NewTable = type("vector_{}".format(name),(Base,),attr_dict)    

    return NewTable

# def generate_variable_table_class(name):
#     """This is a helper function which dynamically creates a new ORM enabled class
#     The table will hold the individual values of each variable
#     Individual values are stored as a string
#     """
# 
#     class NewTable( Base ):
#         __tablename__ = "vector_{}".format(name)
#         id = Column(Integer, primary_key=True)
#         value = Column(String(16), nullable=False, unique=True)
#         def __init__(self,value):
#             self.value = str(value)
#             
#         def __str__(self):
#             return self.value
#         
#         def __repr__(self):
#             return self.value    
#        
#     NewTable.__name__ = "vector_ORM_{}".format(name)
#     
#     return NewTable


if __name__ == "__main__":

    for name in 'asfd', 'jkl', 'xyz':
        print("For loop: ",name)
        #for k in globals():
        #print(globals())
            
        engine = sa.create_engine(r'sqlite:///c:\testdelete\{}.sql'.format(name))
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        #this_foo = Foo(name = 'a')
        #print(this_foo)
        
        #print(Foo)
        #bunch_o_foos = [Foo(name = i) for i in range(10)]
        #session.add_all(bunch_o_foos)
        #session.commit()
        #for foo in bunch_o_foos:
        #    print(foo.id)
        
        this_table = generate_variable_table_class_type("Test")
        print(this_table)
        
        sa.orm.clear_mappers()

        #sa.orm.instrumentation.unregister_class(this_table)
        del this_table._decl_class_registry[this_table.__name__]
    
        
        #variables = [generate_variable_table_class_type(i) for i in range(10)]