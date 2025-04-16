from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON, Date, Time, Float, BigInteger
from sqlalchemy.dialects.postgresql import ARRAY, JSON as PostgresJSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableDict

Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True)
    client_name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    site_name = Column(PostgresJSON, nullable=False)  # Store list of site names as JSON
    greenhouse_name = Column(PostgresJSON, nullable=False)  # Store list of greenhouse names as JSON

'''
class SymptomThreshold(Base):
    __tablename__ = 'symptom_threshold'
    id = Column(Integer, primary_key=True)
    disease = Column(String(10), nullable=False)
    val = Column(Integer, nullable=False)
'''

class CycleInfo(Base):
    __tablename__ = 'cycle-info'
    id = Column(Integer, primary_key=True)
    client_name = Column(String(50), nullable=False)
    site = Column(String(50), nullable=False)
    greenhouse = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    #date = Column(BigInteger, nullable=False)
    #startDate = Column(BigInteger, nullable=False)
    date_date = Column(Date, nullable=False)
    startdate_date = Column(Date, nullable=False)
    observationPending = Column(Boolean, default=False)
    comparedTo = Column(String(50), nullable=True)
    reportwriting = Column(Boolean, default=False)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}





class Greenhouse(Base):
    __tablename__ = 'greenhouse'
    id = Column(Integer, primary_key=True)
    farm_id = Column(Integer, ForeignKey('farm.id'), nullable=False)
    name = Column(String(50), nullable=False)


class EnvData(Base):
    __tablename__ = 'env_data'
    id = Column(Integer, primary_key=True)
    client_name = Column(String(50), nullable=False)
    site = Column(String(50), nullable=False)
    greenhouse_id = Column(Integer, ForeignKey('greenhouse.id'), nullable=False)
    item_id = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    json_data = Column(MutableDict.as_mutable(PostgresJSON), nullable=False)

'''
class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True)
    client_name = Column(String(255))
    selected_cycle = Column(String(255))
    selected_greenhouse = Column(String(255))
    selected_grid = Column(String(255))
    selected_site = Column(String(255))
    message = Column(String)
    fileName = Column(String(255))
    video_status = Column(String(255), default='Pending')
    video_url = Column(String(255), nullable=True)
    '''


class SensorRange(Base):
    __tablename__ = 'sensor_ranges'
    id = Column(Integer, primary_key=True)
    client = Column(String(50))
    greenhouse = Column(String(50))
    site = Column(String(50))
    temp_optimal = Column(String(50))
    humidity_risky = Column(String(50))
    ec_risky = Column(String(50))
    ph_risky = Column(String(50))

    def __repr__(self):
        return f'<SensorRange {self.client}, {self.greenhouse}, {self.site}>'


class DiseaseData(Base):
    __tablename__ = 'disease_data'  # Added tablename since it was missing
    id = Column(Integer, primary_key=True)
    location = Column(String(50), nullable=False)
    crop = Column(String(50), nullable=False)
    disease = Column(String(50), nullable=False)
    temp_range = Column(ARRAY(Float), nullable=True)
    humid_range = Column(ARRAY(Float), nullable=True)
    ec_range = Column(ARRAY(Float), nullable=True)
    ph_range = Column(ARRAY(Float), nullable=True)
    temp_range2 = Column(ARRAY(Float), nullable=True)
    humid_range2 = Column(ARRAY(Float), nullable=True)
    ec_range2 = Column(ARRAY(Float), nullable=True)
    ph_range2 = Column(ARRAY(Float), nullable=True)
    visual_symptom = Column(String(50), nullable=False)

    def to_dict(self):
        return {
            "location": self.location,
            "crop": self.crop,
            "disease": self.disease,
            "temp_range": self.temp_range,
            "humid_range": self.humid_range,
            "ec_range": self.ec_range,
            "ph_range": self.ph_range,
            "temp_range2": self.temp_range2,
            "humid_range2": self.humid_range2,
            "ec_range2": self.ec_range2,
            "ph_range2": self.ph_range2,
            "visual_symptom": self.visual_symptom
        }


class BucketValues(Base):
    __tablename__ = 'bucket_values'  # Added tablename since it was missing
    id = Column(Integer, primary_key=True)
    client_name = Column(String(50), nullable=False)
    site = Column(String(50), nullable=False)
    greenhouse = Column(String(50), nullable=False)
    json_data = Column(PostgresJSON, nullable=False)
    flagarray = Column(PostgresJSON, nullable=False)


class PlantWeek(Base):
    __tablename__ = 'plant_week'
    id = Column(Integer, primary_key=True)
    client_name = Column(String(50), nullable=False)
    site = Column(String(50), nullable=False)
    greenhouse = Column(String(50), nullable=False)
    weekday = Column(Integer, nullable=False)


class Observation(Base):
    __tablename__ = 'observations'
    id = Column(Integer, primary_key=True)
    client_name = Column(String(50), nullable=False)
    site = Column(String(50), nullable=False)
    greenhouse = Column(String(50), nullable=False)
    cycle_name = Column(String(50), nullable=False)
    comparison_cycle_name = Column(String(50), nullable=True)
    delta_t_id = Column(Integer, nullable=False)
    data = Column(PostgresJSON, nullable=True)
    message = Column(PostgresJSON, nullable=True)
    temp_optimal = Column(String(50), nullable=True)
    humidity_optimal = Column(String(50), nullable=True)
    ec_risky = Column(String(50), nullable=True)
    ph_risky = Column(String(50), nullable=True)
    copy = Column(Integer, default=False)
    env_data = Column(PostgresJSON, nullable=True)
    grid_data = Column(PostgresJSON, nullable=True)
    plant_data = Column(PostgresJSON, nullable=True)


class Grid(Base):
    __tablename__ = 'grid_data'
    id = Column(Integer, primary_key=True)
    client_name = Column(String(255))
    selected_greenhouse = Column(String(255))
    selected_site = Column(String(255))
    grid_format = Column(PostgresJSON, nullable=False)


class GridAnalysis(Base):
    __tablename__ = 'grid_analysis'
    id = Column(Integer, primary_key=True)
    client_name = Column(String(255))
    selected_greenhouse = Column(String(255))
    selected_site = Column(String(255))
    selected_cycle = Column(String(255))
    json_data = Column(PostgresJSON, nullable=False)

'''
class FeedBackGridImages(Base):
    __tablename__ = 'feedback_grid_images'
    id = Column(Integer, primary_key=True)
    client_name = Column(String(255))
    selected_greenhouse = Column(String(255))
    selected_site = Column(String(255))
    selected_cycle = Column(String(255))
    selected_grid = Column(String(255))
    json_data = Column(PostgresJSON, nullable=False)
    '''

'''
class Weeks(Base):
    __tablename__ = 'weeks'
    id = Column(Integer, primary_key=True)
    client_name = Column(String(255), nullable=False)
    selected_greenhouse = Column(String(255), nullable=True)
    selected_site = Column(String(255), nullable=True)
    start_cycle = Column(String(255), nullable=True)
    end_cycle = Column(String(255), nullable=True)
    number = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Weeks(id={self.id}, client_name='{self.client_name}', selected_site='{self.selected_site}', selected_greenhouse='{self.selected_greenhouse}')>"

    def to_dict(self):
        """Converts the model instance into a dictionary."""
        return {
            "id": self.id,
            "number": self.number,
            "client_name": self.client_name,
            "selected_greenhouse": self.selected_greenhouse,
            "selected_site": self.selected_site,
            "start_cycle": self.start_cycle,
            "end_cycle": self.end_cycle,
        }
    '''