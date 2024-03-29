import os
import sys

# for path_name in [os.path.join(os.path.dirname(__file__)),
#                   os.path.join(os.path.dirname(__file__), 'features_algorithms'),
#                   os.path.join(os.path.dirname(__file__), 'features_algorithms', 'accelerated_graph_features'),
#                   os.path.join(os.path.dirname(__file__), 'features_algorithms', 'vertices'),
#                   os.path.join(os.path.dirname(__file__), 'features_infra'),
#                   os.path.join(os.path.dirname(__file__), 'graph_infra'),
#                   os.path.join(os.path.dirname(__file__), 'features_meta')
#                   ]:
#     sys.path.append(path_name)

from .features_for_any_graph import FeatureCalculator
from .features_meta import features_meta
from .features_meta import accelerated_features_meta
