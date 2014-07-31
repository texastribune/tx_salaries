from . import alamo_colleges
from . import brownsville_isd
from . import collin_college
from . import dallas_county
from . import eanes_isd
from . import el_paso_county
from . import houston
from . import houston_community_college
from . import state_of_texas
from . import texas_am_system
from . import texas_tech_system
from . import texas_tech_university
from . import ut_austin
from . import ut_arlington
from . import ut_brownsville
from . import ut_dallas
from . import ut_el_paso
from . import ut_health_houston
from . import ut_health_tyler
from . import ut_health_san_antonio
from . import ut_medical_branch
from . import ut_pan_american
from . import ut_permian_basin
from . import ut_san_antonio
from . import ut_system
from . import ut_tyler

TRANSFORMERS = {
    'ddd655aafc883a905a0e2b3556c0e42b34f21d04': [alamo_colleges.transform, ],
    '6e4bb90321c62a34296cad61c3800b1dd308257e': [brownsville_isd.transform, ],
    '39bcb735ae0a6d3b9bddb839337680abf76be1fd': [collin_college.transform, ],
    'c81582dc5ef3233848c0cbe13d9047d2e5a6dbde': [dallas_county.transform, ],
    'b3ac361fd078f04d8035cef647ac839ef3f0f353': [eanes_isd.transform, ],
    'd18ad5c9635a40de15b0ead0e8f8fe97b8ccca31': [el_paso_county.transform, ],
    'fe075cbd88973ebfc8d177dfd27aed40da7088e6': [houston.transform, ],
    'a4f1152500a1c25df0705463266f75a9b15f6b5a': [houston_community_college.transform, ],
    '690fc3890e8f893a7b1634de2df958846ad12a1b': [state_of_texas.transform, ],
    'eb4e22c07597829d7b62f48e6f69dd2d29bf69e2': [texas_am_system.transform, ],
    'bc023bcf9e573ecdf8335ebafb24feec596e473f': [texas_tech_system.transform, ],
    'c60489252da989ab04f6a47a86265dc047dd367b': [texas_tech_university.transform, ],
    '177bf9500b4f73c649e30154c46e0c359d122a48': [
        ('UT System', ut_system.transform),
        ('UT Permian Basin', ut_permian_basin.transform),
        ('UT Austin', ut_austin.transform),
        ('UT Arlington', ut_arlington.transform), ],
    'a1cb75442f33c2f0152296838771087192643869': [ut_brownsville.transform, ],
    '719b1e2e9f6272be76b1fb56bb0f76d779fa1e09': [ut_dallas.transform, ],
    'e0c497dd91f02de6277c121c82667e7db125ba5c': [ut_el_paso.transform, ],
    '92519b7c0eb91165eee92d7154f56c14aa3f2132': [ut_health_houston.transform, ],
    '16355b9afdb4766ce6578d8fbf6f70fd1bb9af47': [ut_health_tyler.transform, ],
    '8ee17cdd4cd042784d2f5a50df1996b0a9f5d731': [ut_health_san_antonio.transform, ],
    'a700c57e47d4c5ae5ec1d2354a0c0ce461c53869': [ut_medical_branch.transform, ],
    'bf2d8d6cad54567327b44050c507096885f925b7': [ut_pan_american.transform, ],
    '3eede716c96db3c302eaa2b9b3af6e176daf7727': [ut_san_antonio.transform, ],
    '068d88f0ea10973339f5a4d57c8d806686d2df40': [ut_tyler.transform, ],
}
