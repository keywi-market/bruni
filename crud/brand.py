from crud import CRUDBase
from models.brand import Brand
from schemas.brand import BrandCreate, BrandUpdate


class CRUDBrand(CRUDBase[Brand, BrandCreate, BrandUpdate]):
    pass


crud_brand = CRUDBrand(Brand)
