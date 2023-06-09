import routers.proposal.models as m, datetime
from pydantic import BaseModel, validator
from typing import Optional, List, Union

class ProposalBase(BaseModel):
    title: str
    justification: str
    department_id: int
    metatitle: Optional[str]
    priority_id: Optional[int]
    description: Optional[str]
    inventory_id: Optional[int]
    status: Optional[m.ProposalStatus]
    author_id: int  # -> get from request

    class Config:
        orm_mode = True

    class Meta:
        model = m.Proposal

class CreateProposal(ProposalBase):
    pass
        
class UpdateProposal(BaseModel):
    priority_id: Optional[int]
    inventory_id: Optional[int]
    department_id: Optional[int]
    procured_asset_id: Optional[int]
    status: Optional[m.ProposalStatus]

    @validator('status') # if item is accepted require inventory to handle procurement
    def _xor_(cls, v, values):
        if v==m.ProposalStatus.accepted:
            if not values['inventory_id']:
                raise ValueError('inventory id required')
        return v

class Proposal(ProposalBase):
    id: int
    created: datetime.datetime
    updated: datetime.datetime    

class ProposalList(BaseModel):
    bk_size: int
    pg_size: int
    data: Union[List[Proposal], list]