from . import alamo_colleges
from . import brownsville_isd
from . import collin_college
from . import eanes_isd
from . import el_paso_county
from . import texas_tech_system
from . import texas_tech_university
from . import potter_county


TRANSFORMERS = {
    'ddd655aafc883a905a0e2b3556c0e42b34f21d04': [alamo_colleges.transform, ],
    '6e4bb90321c62a34296cad61c3800b1dd308257e': [brownsville_isd.transform, ],
    '39bcb735ae0a6d3b9bddb839337680abf76be1fd': [collin_college.transform, ],
    'b3ac361fd078f04d8035cef647ac839ef3f0f353': [eanes_isd.transform, ],
    'd18ad5c9635a40de15b0ead0e8f8fe97b8ccca31': [el_paso_county.transform, ],
    'bc023bcf9e573ecdf8335ebafb24feec596e473f': [texas_tech_system.transform, ],
    'c60489252da989ab04f6a47a86265dc047dd367b': [texas_tech_university.transform, ],
    '0e027f3d0038d81f570cbda2aeedf3dd1f720881': [potter_county.transform, ],
}
