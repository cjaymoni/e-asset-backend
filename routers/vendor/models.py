from sqlalchemy import Column, String, CheckConstraint, Integer, ForeignKey
from sqlalchemy.orm import validates, relationship
from constants import EMAIL, PHONE
from database import TenantBase, Base
from mixins import BaseMixin
import re

# from routers.category.models import CategoryVendor

class Vendor(BaseMixin, TenantBase):
    '''Vendor Model'''
    __tablename__ = "vendors"
    __table_args__ = (CheckConstraint('coalesce(contact , email) is not null', name='_email_or_contact_'),)

    title =  Column(String, nullable=False)
    website = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    contact = Column(String, unique=True, nullable=True)
    assets_sold = relationship("Asset", back_populates="vendor")
    # categories = relationship(Category,  back_populates="categories")
    # category_id = Column(Integer, ForeignKey('%s.categories.id'%Base.metadata.schema))
    category_id = Column(Integer, ForeignKey('%s.categories.id'%Base.metadata.schema))
    # secondary=CategoryVendor.__table__,

    @validates('email')
    def validate_email(self, key, address):
        assert re.search(EMAIL, address), 'invalid email format'
        return address
    
    @validates('contact')
    def validate_phone(self, key, address):
        assert re.search(PHONE, address), 'invalid phone format'
        return address

print('%s.categories.id'%Base.metadata.schema)