from sqlalchemy import Column, Integer, String, Float,ForeignKey,Table
from sqlalchemy.orm import DeclarativeBase,relationship

class Base(DeclarativeBase):
    pass

package_truck = Table("package_truck",Base.metadata,
                      Column("package_id",Integer,ForeignKey("packages.id"),primary_key=True),
                      Column("truck_id",Integer,ForeignKey("trucks.id"),primary_key=True))

class Warehouse(Base):
    __tablename__ = "warehouses"
    id = Column(Integer,primary_key=True,autoincrement=True)
    warehouse_name = Column(String(255), nullable=False)
    location = Column(String(255),nullable=False)
    package = relationship("Package", back_populates="warehouses")


class Package(Base):
    __tablename__ = "packages"
    id = Column(Integer,primary_key=True,autoincrement=True)
    weight = Column(Float,nullable=False)
    warehouse_id = Column(Integer,ForeignKey("warehouses.id"),nullable=False)
    warehouse = relationship("Warehouse",back_populates="packages")
    truck = relationship("Truck",back_populates="packages",secondary=package_truck)

class Waybill(Base):
    __tablename__ = "waybills"
    id = Column(Integer,primary_key=True,autoincrement=True)
    tracking_number = Column(String(255), nullable=False,unique=True)
    shipping_status = Column(String(255), nullable=False)
    package_id = Column(Integer, ForeignKey("packages.id"),unique=True)
    package = relationship("Package", back_populates="waybills",uselist=False)

class Truck(Base):
    __tablename__ = "trucks"
    id = Column(Integer,primary_key=True,autoincrement=True)
    license_plate =  Column(String(255), nullable=False,unique=True)
    package = relationship("Package",back_populates="trucks", secondary=package_truck)