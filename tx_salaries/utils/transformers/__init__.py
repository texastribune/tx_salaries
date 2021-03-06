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
    '9eec7552e7042c434b20f34aa4aa9fd87bb3228e': [allen_isd.transform, ],
    '245256cd03b1ce7f9f076c578f1f4d5be16ff4ee': [austin.transform, ],
    'ee4ad65260cc250e6a52b9728d45efa871fead0b': [austin_community_college.transform, ],
    '2a51198f9949fc5d13a90f048b3a9eb7a8c1c0de': [austin_isd.transform, ],
    '977015f0f9ef0fe0f99138b912b31b4f31c3aff1': [beaumont_isd.transform, ],
    'da2a22ec28df5fa21a018fb237edee71a3549b6b': [bexar_county.transform, ],
    '6e4bb90321c62a34296cad61c3800b1dd308257e': [brownsville_isd.transform, ],
    '2ec7de74cf3768a517adfbe035b1c6436f353649': [bryan_isd.transform, ],
    'bbeaab35571afadf074586ef3d75f739a4dfe471': [college_station_isd.transform, ],
    '39bcb735ae0a6d3b9bddb839337680abf76be1fd': [collin_college.transform, ],
    '2978e84159d1ce3bc77f66a679f385ba6cbadb73': [cypress_fairbanks_isd.transform, ],
    '95d6d9a4f8a38137a69ba2031b0b96bf19a8a74a': [dallas.transform, ],
    '361f2e1b29ca902008de1e291ad98ed134f4eea7': [dallas_county_comm_college.transform, ],
    '5fb77188fdfa1b6a1d794754ffb1c9a9bf69a171': [dallas_county.transform, ],
    '75e1bfa34014b500ab194c557b686fa1ca021afc': [dallas_isd.transform, ],
    'b3ac361fd078f04d8035cef647ac839ef3f0f353': [eanes_isd.transform, ],
    'd18ad5c9635a40de15b0ead0e8f8fe97b8ccca31': [el_paso_county.transform, ],
    '578a8bb56581d0cae8154b26286abc93f2bf093a': [fort_worth.transform, ],
    'a9c48289c0c112b10e91baca6cf42159597f2c6d': [hays_county.transform, ],
    '4b2cfddf28abd34cbd7e3fbc36505a8099197934': [houston.transform, ],
    'a4f1152500a1c25df0705463266f75a9b15f6b5a': [houston_community_college.transform, ],
    'c81cfde5a929b4641b8890330287a7c592640211': [houston_isd.transform, ],
    '9e98eb0c70037636d678c201e03173ce66c5bc4f': [katy_isd.transform, ],
    'd982fa55bf19391e9f756cf03614cdd3969c4311': [north_east_isd.transform, ],
    '10339a3c4cc7dfb78c7120fc5a92da052062ccc5': [mcallen_isd.transform, ],
    '87a9564706644a2287ad4cd16cdddf8c330b0af0': [metropolitan_transit_authority.transform, ],
    'c98e393bf1b3fc2635b31fcedb0cfbc69766e5ac': [midwestern_state_university.transform, ],
    '2252263014de05fa4efd240e0a3716c484495a93': [pasadena_isd.transform, ],
    '0e027f3d0038d81f570cbda2aeedf3dd1f720881': [potter_county.transform, ],
    '5feb4b052c707d25812b95bff1d2ce851e4773c4': [san_antonio.transform, ],
    '2412f56c1cbced970ab823b9603a082778a0b3b1': [rockwall_isd.transform, ],
    '88babff77c8f0e458b53b2cec3945f213560832f': [state_of_texas.transform, ],
    'f6f34e7019ffbe0180962e18b80a380973509f94': [tarrant_county.transform, ],
    'ba91bb9dc1a2e1359ff3ca96d024b66d2e01e65f': [tarrant_comm_college.transform, ],
    'a6f58e9f74ec0afae72b954668b620d6d7baba23': [texas_am_system.transform, ],
    '04f3e0ad1d1b1e59b61e9d8c29b8ba572a2ef17c': [texas_state_university.transform, ],
    'bc023bcf9e573ecdf8335ebafb24feec596e473f': [texas_tech_system.transform, ],
    'c60489252da989ab04f6a47a86265dc047dd367b': [texas_tech_university.transform, ],
    '69c230c1c29f5d7c64cedd3c14ffe6d149f6bad3': [texas_tech_university_hsc.transform, ],
    '63ca4b9cd0465cb3daaad24b070689a0c065d863': [texas_womans_university.transform, ],
    'd511e81acc629e5d701826885dfb4c6a1181ef05': [travis_county.transform, ],
    '4f2ba9ac90a8d19bbe39aec36c718e84d5d3a772': [university_of_houston.transform, ],
    'cc53178eb3453667e07593476ce27457db5fea34': [ut_arlington.transform, ],
    '30c0ee0b76df0b8ae4007901f38af1e959acd889': [university_of_north_texas_system.transform, ],
    'feda3832b236e9e4c5245d1088809f0695e5635c': [ut_austin.transform, ],
    'a1cb75442f33c2f0152296838771087192643869': [ut_brownsville.transform, ],
    '1d67811bdfeccbc7d4464c7090d1e4544b352c54': [ut_dallas.transform, ],
    '95c080874ae706054f88c041d7aed5b9044d2960': [ut_el_paso.transform, ],
    'c287128e946a27ddf6ee32a033c68d0f69607a32': [ut_health_houston.transform, ],
    '016ea020af8d794acb552fc1f7494a9649fb3c92': [ut_health_northeast.transform, ],
    '4d7ccbcd2807a9841717b6fa5d868b8799e72274': [ut_health_san_antonio.transform, ],
    '880d2a6382396199db040f3f5f631d20608c489f': [ut_md_anderson.transform, ],
    '6de7d3493606387d479d707ac414dcdf3f7fa402': [ut_medical_branch.transform, ],
    'bf2d8d6cad54567327b44050c507096885f925b7': [ut_pan_american.transform, ],
    '20800a924b339cac56328d201c6ed318534193ff': [ut_permian_basin.transform, ],
    '00e36d75c87e700584d1ab70fe1f8c9b39f58bbb': [ut_san_antonio.transform, ],
    '86f7d5e59772f88ebe483a5383fb07617f9dc4f3': [ut_tyler.transform, ],
    'ec2e93286df0335f4100f6550278ce8d128397dd': [ut_system.transform, ],
    '5714aa39bed15a7d032097c2aa0be7df68507e56': [ut_southwestern.transform, ],
    '0c43b8c9dbcb65ab659a4f9b5e017fdd3794daca': [ut_southwestern_mc.transform, ],
    'fd66132338a69d2fb76faa1d91b6f0d21ffc5aec': [ut_san_antonio.transform, ],
    '068d88f0ea10973339f5a4d57c8d806686d2df40': [ut_tyler.transform, ],
    '82fbe7f20bd25bf024dfd909f0370de9f8427a62': [williamson_county.transform, ]
}
