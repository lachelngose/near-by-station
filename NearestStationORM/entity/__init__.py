from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Numeric, Float, Date, String, Boolean
from sqlalchemy.dialects.postgresql import ARRAY, JSON, JSONB

Base = declarative_base()


class Article(Base):
    __tablename__ = 'article_master'

    code = Column(String, nullable=False, primary_key=True)
    pnu = Column(String)
    full_address = Column(String, nullable=False)
    si_address = Column(String, nullable=False)
    gu_address = Column(String, nullable=False)
    road_name_address = Column(String, nullable=False)
    expose_start_date = Column(Date, nullable=False)
    current_deal_price = Column(Numeric, nullable=False)
    current_unit_price = Column(Numeric, nullable=False)
    prev_deal_price = Column(Numeric)
    cp_pc_article_url = Column(String, nullable=False)
    is_detail_address = Column(Boolean, nullable=False)
    lat = Column("latitude", Float, nullable=False)
    lng = Column("longitude", Float, nullable=False)
    geometry = Column(JSON, nullable=False)
    floor_cnt = Column(Numeric)
    ungflr_cnt = Column(Numeric)
    age = Column(Integer)
    use_nm = Column(String)
    gf_ar = Column(Numeric)
    far_gf_ar = Column(Numeric)
    jimok = Column(String)
    landuse_zone_nm = Column(String, nullable=False)
    img_urls = Column(ARRAY(String), nullable=False)
    img_description = Column(String)
    est_price = Column(Numeric, nullable=False)
    est_lower_price = Column(Numeric, nullable=False)
    est_upper_price = Column(Numeric, nullable=False)
    connection_area = Column(Numeric, nullable=False)
    show_order = Column(Numeric, nullable=False)
    ground_space = Column(Numeric, nullable=False)
    sales_item_id = Column(String)

    def __init__(self,
                 code, pnu, full_address, si_address, gu_address, road_name_address, expose_start_date,
                 current_deal_price, current_unit_price, prev_deal_price, cp_pc_article_url, is_detail_address,
                 latitude, longitude, geometry, floor_cnt, ungflr_cnt, age, use_nm, gf_ar, far_gf_ar, jimok,
                 landuse_zone_nm, img_urls, img_description, est_price, est_lower_price, est_upper_price,
                 connection_area, show_order, ground_space, sales_item_id):
        self.code = code
        self.pnu = pnu
        self.full_address = full_address
        self.si_address = si_address
        self.gu_address = gu_address
        self.road_name_address = road_name_address
        self.expose_start_date = expose_start_date
        self.current_deal_price = current_deal_price
        self.current_unit_price = current_unit_price
        self.prev_deal_price = prev_deal_price
        self.cp_pc_article_url = cp_pc_article_url
        self.is_detail_address = is_detail_address
        self.lat = latitude
        self.lng = longitude
        self.geometry = geometry
        self.floor_cnt = floor_cnt
        self.ungflr_cnt = ungflr_cnt
        self.age = age
        self.use_nm = use_nm
        self.gf_ar = gf_ar
        self.far_gf_ar = far_gf_ar
        self.jimok = jimok
        self.landuse_zone_nm = landuse_zone_nm
        self.img_urls = img_urls
        self.img_description = img_description
        self.est_price = est_price
        self.est_lower_price = est_lower_price
        self.est_upper_price = est_upper_price
        self.connection_area = connection_area
        self.show_order = show_order
        self.ground_space = ground_space
        self.sales_item_id = sales_item_id

    def __getitem__(self, key):
        return getattr(self, key)


class Station(Base):
    __tablename__ = 'station_coordinate'

    id = Column(Integer, nullable=False, primary_key=True)
    line = Column(String)
    name = Column(String)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)

    def __init__(self, id, line, name, lat, lng):
        self.id = id
        self.line = line
        self.name = name
        self.lat = lat
        self.lng = lng

    def __getitem__(self, key):
        return getattr(self, key)


class NearByStationInfo(Base):
    __tablename__ = 'nearby_station_info'

    pnu = Column(String, nullable=False, primary_key=True)
    station_id = Column(Integer, nullable=False, primary_key=True)
    station_line = Column(String)
    station_name = Column(String)
    distance = Column(Numeric, nullable=False)
    consuming_time = Column(Numeric, nullable=False)
    route = Column(ARRAY(JSONB))

    def __init__(self, pnu, station_id, station_line, station_name, distance, consuming_time, route):
        self.pnu = pnu
        self.station_id = station_id
        self.station_line = station_line
        self.station_name = station_name
        self.distance = distance
        self.consuming_time = consuming_time
        self.route = route
