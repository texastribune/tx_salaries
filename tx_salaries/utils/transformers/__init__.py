from . import alamo_colleges
from . import allen_isd
from . import austin_community_college
from . import austin_isd
from . import austin
from . import beaumont_isd
from . import bexar_county
from . import brownsville_isd
from . import bryan_isd
from . import cypress_fairbanks_isd
from . import college_station_isd
from . import collin_college
from . import dallas
from . import dallas_county_comm_college
from . import dallas_county
from . import dallas_isd
from . import eanes_isd
from . import el_paso_county
from . import fort_worth
from . import hays_county
from . import houston
from . import houston_community_college
from . import katy_isd
from . import mcallen_isd
from . import metropolitan_transit_authority
from . import midwestern_state_university
from . import north_east_isd
from . import pasadena_isd
from . import potter_county
from . import san_antonio
from . import rockwall_isd
from . import state_of_texas
from . import tarrant_comm_college
from . import tarrant_county
from . import texas_am_system
from . import texas_state_university
from . import texas_tech_system
from . import texas_tech_university
from . import texas_tech_university_hsc
from . import university_of_houston
from . import texas_womans_university
from . import travis_county
from . import university_of_north_texas_system
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
from . import ut_southwestern
from . import ut_system
from . import ut_tyler
from . import williamson_county

TRANSFORMERS = {
    'ddd655aafc883a905a0e2b3556c0e42b34f21d04': [alamo_colleges.transform, ],
    '7c54a167e6d77023b08aa5c5566a434bb34c0357': [allen_isd.transform, ],
    'ee4ad65260cc250e6a52b9728d45efa871fead0b': [austin_community_college.transform, ],
    '2a51198f9949fc5d13a90f048b3a9eb7a8c1c0de': [austin_isd.transform, ],
    'd626664c9fb1d8c3e691777f14bb69775cb0abe9': [austin.transform, ],
    '129db1bc7003a42783d41a3b0d9cf0db77e1c76b': [beaumont_isd.transform, ],
    '215681115c43dc1e1e6f9e14d824c96e31b6144a': [bexar_county.transform, ],
    '6e4bb90321c62a34296cad61c3800b1dd308257e': [brownsville_isd.transform, ],
    '2ec7de74cf3768a517adfbe035b1c6436f353649': [bryan_isd.transform, ],
    'bbeaab35571afadf074586ef3d75f739a4dfe471': [college_station_isd.transform, ],
    '39bcb735ae0a6d3b9bddb839337680abf76be1fd': [collin_college.transform, ],
    '3f7de7d31ca62454e6e8b9c8e9e88174d88790b8': [cypress_fairbanks_isd.transform, ],
    '95e5f3c47affecfb924230ce117cfb88599c2368': [dallas.transform, ],
    '695426d2122576c140691958c145818d31f95c89': [dallas_county_comm_college.transform, ],
    'eb61956148a1c009ab8f5275650b279531f970d6': [dallas_county.transform, ],
    '9cd2f59f4b4ec7b7b1fbf5b0da6571a671d22662': [dallas_isd.transform, ],
    'b3ac361fd078f04d8035cef647ac839ef3f0f353': [eanes_isd.transform, ],
    'd18ad5c9635a40de15b0ead0e8f8fe97b8ccca31': [el_paso_county.transform, ],
    '578a8bb56581d0cae8154b26286abc93f2bf093a': [fort_worth.transform, ],
    'a9c48289c0c112b10e91baca6cf42159597f2c6d': [hays_county.transform, ],
    'b91a9f78c4db005d73b11c228f30657ced7ed3c7': [houston.transform, ],
    'a4f1152500a1c25df0705463266f75a9b15f6b5a': [houston_community_college.transform, ],
    '63756f881651e50857ed321b897b34a6440b47c6': [katy_isd.transform, ],
    'd982fa55bf19391e9f756cf03614cdd3969c4311': [north_east_isd.transform, ],
    '10339a3c4cc7dfb78c7120fc5a92da052062ccc5': [mcallen_isd.transform, ],
    '87a9564706644a2287ad4cd16cdddf8c330b0af0': [metropolitan_transit_authority.transform, ],
    'c98e393bf1b3fc2635b31fcedb0cfbc69766e5ac': [midwestern_state_university.transform, ],
    '2252263014de05fa4efd240e0a3716c484495a93': [pasadena_isd.transform, ],
    '0e027f3d0038d81f570cbda2aeedf3dd1f720881': [potter_county.transform, ],
    'f53125485535c4619b16838160dc4bd41875389f': [san_antonio.transform, ],
    '2412f56c1cbced970ab823b9603a082778a0b3b1': [rockwall_isd.transform, ],
    'fe04a26f9020282230d1a133d0f1a5c00a264b62': [state_of_texas.transform, ],
    '2aaf4d7f6687edfb719e84bd4a370c49425399b7': [tarrant_county.transform, ],
    '5f34613a2026006655ae15c0e31e8ed4f5ef29fa': [tarrant_comm_college.transform, ],
    'e1af1d516d482dc89008704156ed2cc4e40ea18e': [texas_am_system.transform, ],
    '04f3e0ad1d1b1e59b61e9d8c29b8ba572a2ef17c': [texas_state_university.transform, ],
    'bc023bcf9e573ecdf8335ebafb24feec596e473f': [texas_tech_system.transform, ],
    'c60489252da989ab04f6a47a86265dc047dd367b': [texas_tech_university.transform, ],
    '6ed63202860363b3add42ec5418c00c73efe96ac': [texas_tech_university_hsc.transform, ],
    '63ca4b9cd0465cb3daaad24b070689a0c065d863': [texas_womans_university.transform, ],
    'facd5bf54a4a075309fd32b2e1931e3a939d325e': [travis_county.transform, ],
    '67d1306dcef659d2e9df5b080e70a326b5dcc178': [ut_arlington.transform, ],
    '0578da0ef48fcbf96a52b96798397460c6f286d5': [university_of_houston.transform, ],
    '30c0ee0b76df0b8ae4007901f38af1e959acd889': [university_of_north_texas_system.transform, ],
    '2115235d43a6f292c7a37e26e12cd0e77a683a1a': [ut_austin.transform, ],
    'a1cb75442f33c2f0152296838771087192643869': [ut_brownsville.transform, ],
    '1d67811bdfeccbc7d4464c7090d1e4544b352c54': [ut_dallas.transform, ],
    '7a3671ec33d3ca63ee3aa9b532e42c36f616e56c': [ut_el_paso.transform, ],
    '4df8b9322ef4273b4613d57449b314a0d05c8713': [ut_health_houston.transform, ],
    '6f13d4a1fd50874ee952b4f07058d027c9ef2a44': [ut_health_northeast.transform, ],
    '16355b9afdb4766ce6578d8fbf6f70fd1bb9af47': [ut_health_tyler.transform, ],
    '2af31c303e013d25eeb1d1e68281aae30e090f8f': [ut_health_san_antonio.transform, ],
    'bba2c6a05fee0a4a1adf771686c66c4797665c4b': [ut_md_anderson.transform, ],
    '258ae8c47dc5b5bd842fb82569b1be7ba8c1bd7d': [ut_medical_branch.transform, ],
    'bf2d8d6cad54567327b44050c507096885f925b7': [ut_pan_american.transform, ],
    'dc125c8ca1bdfbe9888abefcb2806064d5b6b55d': [ut_permian_basin.transform, ],
    '3eede716c96db3c302eaa2b9b3af6e176daf7727': [ut_san_antonio.transform, ],
    'de0167927d7162fb025b72c76a1fc157f081c00b': [ut_tyler.transform, ],
    'fe980380568d4efbc398522dfd71a3e872ea33ac': [ut_system.transform, ],
    '5714aa39bed15a7d032097c2aa0be7df68507e56': [ut_southwestern.transform, ],
    'fd66132338a69d2fb76faa1d91b6f0d21ffc5aec': [ut_san_antonio.transform, ],
    '068d88f0ea10973339f5a4d57c8d806686d2df40': [ut_tyler.transform, ],
    '82fbe7f20bd25bf024dfd909f0370de9f8427a62': [williamson_county.transform, ]
}
