from . import alamo_colleges
from . import allen_isd
from . import austin_isd
from . import austin
from . import beaumont_isd
from . import brownsville_isd
from . import collin_college
from . import dallas
from . import dallas_county
from . import eanes_isd
from . import el_paso_county
from . import houston
from . import houston_community_college
from . import katy_isd
from . import metropolitan_transit_authority
from . import midwestern_state_university
from . import north_east_isd
from . import pasadena_isd
from . import potter_county
from . import san_antonio
from . import rockwall_isd
from . import state_of_texas
from . import tarrant_county
from . import texas_am_system
from . import texas_state_university
from . import texas_tech_system
from . import texas_tech_university
from . import texas_womans_university
from . import ut_austin
from . import ut_arlington
from . import ut_brownsville
from . import ut_dallas
from . import ut_el_paso
from . import ut_health_houston
from . import ut_health_northeast
from . import ut_health_tyler
from . import ut_health_san_antonio
from . import ut_md_anderson
from . import ut_medical_branch
from . import ut_pan_american
from . import ut_permian_basin
from . import ut_san_antonio
from . import ut_system
from . import ut_tyler

TRANSFORMERS = {
    'ddd655aafc883a905a0e2b3556c0e42b34f21d04': [alamo_colleges.transform, ],
    'f0d7f1733d2e76dc76f2aaea9ad7f6babf824975': [allen_isd.transform, ],
    '2a51198f9949fc5d13a90f048b3a9eb7a8c1c0de': [austin_isd.transform, ],
    '3c71e58afb5d003074a2b7a196133ca28b4e0e3d': [austin.transform, ],
    'fc0eb7927ee4d39dab7602f01ab771eb49eb7512': [beaumont_isd.transform, ],
    '6e4bb90321c62a34296cad61c3800b1dd308257e': [brownsville_isd.transform, ],
    '39bcb735ae0a6d3b9bddb839337680abf76be1fd': [collin_college.transform, ],
    '1a55d6050f034d84f6551cd629e46805c8788297': [dallas.transform, ],
    'c81582dc5ef3233848c0cbe13d9047d2e5a6dbde': [dallas_county.transform, ],
    'b3ac361fd078f04d8035cef647ac839ef3f0f353': [eanes_isd.transform, ],
    'd18ad5c9635a40de15b0ead0e8f8fe97b8ccca31': [el_paso_county.transform, ],
    'fe075cbd88973ebfc8d177dfd27aed40da7088e6': [houston.transform, ],
    'a4f1152500a1c25df0705463266f75a9b15f6b5a': [houston_community_college.transform, ],
    '0809eca5428e583732e7939f7252398f5c4e6947': [katy_isd.transform, ],
    'd982fa55bf19391e9f756cf03614cdd3969c4311': [north_east_isd.transform, ],
    'd84e2b3a0005d7d80672ccc80f5793cd07981439': [metropolitan_transit_authority.transform, ],
    '7af76c3e173736d45290ba2d657230a111dfd572': [midwestern_state_university.transform, ],
    '2252263014de05fa4efd240e0a3716c484495a93': [pasadena_isd.transform, ],
    '0e027f3d0038d81f570cbda2aeedf3dd1f720881': [potter_county.transform, ],
    'f53125485535c4619b16838160dc4bd41875389f': [san_antonio.transform, ],
    '5034d589091e79d58ee3c51766bd6ab05f08d3a5': [rockwall_isd.transform, ],
    '690fc3890e8f893a7b1634de2df958846ad12a1b': [state_of_texas.transform, ],
    '96c50536164eeecade2194082544648d3bb4fd97': [tarrant_county.transform, ],
    'e1af1d516d482dc89008704156ed2cc4e40ea18e': [texas_am_system.transform, ],
    '3382282e79ee58627aedd4703591928b09525af5': [texas_state_university.transform, ],
    'bc023bcf9e573ecdf8335ebafb24feec596e473f': [texas_tech_system.transform, ],
    'c60489252da989ab04f6a47a86265dc047dd367b': [texas_tech_university.transform, ],
    '63ca4b9cd0465cb3daaad24b070689a0c065d863': [texas_womans_university.transform, ],
    '177bf9500b4f73c649e30154c46e0c359d122a48': [
        ('UT System', ut_system.transform),
        ('UT Permian Basin', ut_permian_basin.transform),
        ('UT Arlington', ut_arlington.transform), ],
    '2115235d43a6f292c7a37e26e12cd0e77a683a1a': [ut_austin.transform, ],
    'a1cb75442f33c2f0152296838771087192643869': [ut_brownsville.transform, ],
    '1124210f0bdca6e3713c422117cd721e38bff3cb': [ut_dallas.transform, ],
    'e0c497dd91f02de6277c121c82667e7db125ba5c': [ut_el_paso.transform, ],
    '05673091618034bf2f3c1aa338669cc5a57894c2': [ut_health_houston.transform, ],
    '6f13d4a1fd50874ee952b4f07058d027c9ef2a44': [ut_health_northeast.transform, ],
    '16355b9afdb4766ce6578d8fbf6f70fd1bb9af47': [ut_health_tyler.transform, ],
    '8ee17cdd4cd042784d2f5a50df1996b0a9f5d731': [ut_health_san_antonio.transform, ],
    'a70e63dd99026dd7ca0d9c5cd6a17fea15f261a7': [ut_md_anderson.transform, ],
    '258ae8c47dc5b5bd842fb82569b1be7ba8c1bd7d': [ut_medical_branch.transform, ],
    'bf2d8d6cad54567327b44050c507096885f925b7': [ut_pan_american.transform, ],
    'fd66132338a69d2fb76faa1d91b6f0d21ffc5aec': [ut_san_antonio.transform, ],
    '068d88f0ea10973339f5a4d57c8d806686d2df40': [ut_tyler.transform, ],
}
