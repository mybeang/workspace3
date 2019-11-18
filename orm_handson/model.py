from orm_handson.database import Base

from sqlalchemy import Column, String, Integer, Sequence



class Result(Base):
    __tablename__ = 'results'

    num = Column(Integer, Sequence('num_seq'), primary_key=True)
    vender = Column(String)
    model = Column(String)
    serialnumber = Column(String)
    barcode = Column(String)
    date = Column(String)
    memory = Column(String)
    cpu = Column(String)
    traffic = Column(String)
    port = Column(String)
    final = Column(String)
    nos = Column(String)
    config = Column(String)

    def __init__(self, num, vender, model, serialnumber, barcode, date,
                 memory, cpu, traffic, port, final, nos, config):
        self.num = num
        self.vender = vender
        self.model = model
        self.serialnumber = serialnumber
        self.barcode = barcode
        self.date = date
        self.memory = memory
        self.cpu = cpu
        self.traffic = traffic
        self.port = port
        self.final = final
        self.nos = nos
        self.config = config

    def __repr__(self):
        return "<Result('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (
            self.num, self.vender, self.model, self.serialnumber, self.barcode, self.date,
            self.memory, self.cpu, self.traffic, self.port, self.final, self.nos, self.config
        )

    def to_dict(self):
        return {
            'num': self.num,
            'vender': self.vender,
            'model': self.model,
            'serialnumber': self.serialnumber,
            'barcode': self.barcode,
            'date': self.date,
            'memory': self.memory,
            'cpu': self.cpu,
            'traffic': self.traffic,
            'port': self.port,
            'final': self.final,
            'nos': self.nos,
            'config': self.config
        }