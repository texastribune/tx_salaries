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
from . import houston_isd
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
from . import ut_health_san_antonio
from . import ut_md_anderson
from . import ut_medical_branch
from . import ut_pan_american
from . import ut_permian_basin
from . import ut_san_antonio
from . import ut_southwestern
from . import ut_southwestern_mc
from . import ut_system
from . import ut_tyler
from . import williamson_county

TRANSFORMERS = {
    'ddd655aafc883a905a0e2b3556c0e42b34f21d04': [alamo_colleges.transform, ],
    '7c54a167e6d77023b08aa5c5566a434bb34c0357': [allen_isd.transform, ],
    '245256cd03b1ce7f9f076c578f1f4d5be16ff4ee': [austin.transform, ],
    'ee4ad65260cc250e6a52b9728d45efa871fead0b': [austin_community_college.transform, ],
    '2a51198f9949fc5d13a90f048b3a9eb7a8c1c0de': [austin_isd.transform, ],
    '129db1bc7003a42783d41a3b0d9cf0db77e1c76b': [beaumont_isd.transform, ],
    '215681115c43dc1e1e6f9e14d824c96e31b6144a': [bexar_county.transform, ],
    '6e4bb90321c62a34296cad61c3800b1dd308257e': [brownsville_isd.transform, ],
    '2ec7de74cf3768a517adfbe035b1c6436f353649': [bryan_isd.transform, ],
    'bbeaab35571afadf074586ef3d75f739a4dfe471': [college_station_isd.transform, ],
    '39bcb735ae0a6d3b9bddb839337680abf76be1fd': [collin_college.transform, ],
    '2978e84159d1ce3bc77f66a679f385ba6cbadb73': [cypress_fairbanks_isd.transform, ],
    '95e5f3c47affecfb924230ce117cfb88599c2368': [dallas.transform, ],
    '361f2e1b29ca902008de1e291ad98ed134f4eea7': [dallas_county_comm_college.transform, ],
    '5fb77188fdfa1b6a1d794754ffb1c9a9bf69a171': [dallas_county.transform, ],
    '75e1bfa34014b500ab194c557b686fa1ca021afc': [dallas_isd.transform, ],
    'b3ac361fd078f04d8035cef647ac839ef3f0f353': [eanes_isd.transform, ],
    'd18ad5c9635a40de15b0ead0e8f8fe97b8ccca31': [el_paso_county.transform, ],
    '578a8bb56581d0cae8154b26286abc93f2bf093a': [fort_worth.transform, ],
    'a9c48289c0c112b10e91baca6cf42159597f2c6d': [hays_county.transform, ],
    'e5f6cf05268ab2b6198dfa297d40f87f59f5c3d7': [houston.transform, ],
    'a4f1152500a1c25df0705463266f75a9b15f6b5a': [houston_community_college.transform, ],
    'c81cfde5a929b4641b8890330287a7c592640211': [houston_isd.transform, ],
    '63756f881651e50857ed321b897b34a6440b47c6': [katy_isd.transform, ],
    'd982fa55bf19391e9f756cf03614cdd3969c4311': [north_east_isd.transform, ],
    '10339a3c4cc7dfb78c7120fc5a92da052062ccc5': [mcallen_isd.transform, ],
    '87a9564706644a2287ad4cd16cdddf8c330b0af0': [metropolitan_transit_authority.transform, ],
    'c98e393bf1b3fc2635b31fcedb0cfbc69766e5ac': [midwestern_state_university.transform, ],
    '2252263014de05fa4efd240e0a3716c484495a93': [pasadena_isd.transform, ],
    '0e027f3d0038d81f570cbda2aeedf3dd1f720881': [potter_county.transform, ],
    '465604c88252932722ac0ed913354d54e8780b69': [san_antonio.transform, ],
    '2412f56c1cbced970ab823b9603a082778a0b3b1': [rockwall_isd.transform, ],
    '726e9866bf87f07b036ea66116653a75083c29b9': [state_of_texas.transform, ],
    '2aaf4d7f6687edfb719e84bd4a370c49425399b7': [tarrant_county.transform, ],
    'ba91bb9dc1a2e1359ff3ca96d024b66d2e01e65f': [tarrant_comm_college.transform, ],
    'e1af1d516d482dc89008704156ed2cc4e40ea18e': [texas_am_system.transform, ],
    '04f3e0ad1d1b1e59b61e9d8c29b8ba572a2ef17c': [texas_state_university.transform, ],
    'bc023bcf9e573ecdf8335ebafb24feec596e473f': [texas_tech_system.transform, ],
    'c60489252da989ab04f6a47a86265dc047dd367b': [texas_tech_university.transform, ],
    '69c230c1c29f5d7c64cedd3c14ffe6d149f6bad3': [texas_tech_university_hsc.transform, ],
    '63ca4b9cd0465cb3daaad24b070689a0c065d863': [texas_womans_university.transform, ],
    'd511e81acc629e5d701826885dfb4c6a1181ef05': [travis_county.transform, ],
    '67d1306dcef659d2e9df5b080e70a326b5dcc178': [ut_arlington.transform, ],
    '7ffb43ec6298e629cde3be3118a16d15ee11e36f': [university_of_houston.transform, ],
    '30c0ee0b76df0b8ae4007901f38af1e959acd889': [university_of_north_texas_system.transform, ],
    '635e2f22442ecacad7e7028951ed6f61a7f07671': [ut_austin.transform, ],
    'a1cb75442f33c2f0152296838771087192643869': [ut_brownsville.transform, ],
    '1d67811bdfeccbc7d4464c7090d1e4544b352c54': [ut_dallas.transform, ],
    '7a3671ec33d3ca63ee3aa9b532e42c36f616e56c': [ut_el_paso.transform, ],
    'c287128e946a27ddf6ee32a033c68d0f69607a32': [ut_health_houston.transform, ],
    '016ea020af8d794acb552fc1f7494a9649fb3c92': [ut_health_northeast.transform, ],
    '128e3b2ced272388068fa4066305968e1068cf3f': [ut_health_san_antonio.transform, ],
    '4a6620f449d5653a0a5372f9ab5f9d85befa2ec8': [ut_md_anderson.transform, ],
    '7d89fdb0178d051e02bc77bf74f1542e59e0ce25': [ut_medical_branch.transform, ],
    'bf2d8d6cad54567327b44050c507096885f925b7': [ut_pan_american.transform, ],
    '20800a924b339cac56328d201c6ed318534193ff': [ut_permian_basin.transform, ],
    '00e36d75c87e700584d1ab70fe1f8c9b39f58bbb': [ut_san_antonio.transform, ],
    '86f7d5e59772f88ebe483a5383fb07617f9dc4f3': [ut_tyler.transform, ],
    'ec2e93286df0335f4100f6550278ce8d128397dd': [ut_system.transform, ],
    '5714aa39bed15a7d032097c2aa0be7df68507e56': [ut_southwestern.transform, ],
    '6121ff820451267363efe09a1249154334e4afb0': [ut_southwestern_mc.transform, ],
    'fd66132338a69d2fb76faa1d91b6f0d21ffc5aec': [ut_san_antonio.transform, ],
    '068d88f0ea10973339f5a4d57c8d806686d2df40': [ut_tyler.transform, ],
    '82fbe7f20bd25bf024dfd909f0370de9f8427a62': [williamson_county.transform, ]
}
