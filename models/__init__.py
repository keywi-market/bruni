from .product import *
# Entity만 가지고 테이블 생성 시 Aggregate Root 인 Entity가 상위에 있어야 먼저 생성 되고, 이후에 하위 Entity 테이블이 생성 된다.
# Category.__table__.create(engine)
# Brand.__table__.create(engine)
from .category import *
from .brand import *
