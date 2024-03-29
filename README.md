# Topological Graph Features

Topological feature calculators infrastructure.

## Calculating Features
This package helps one to calculate features for a given graph. All features are implemented in python codes, 
and some features have also an accelerated version written in C++. Among the accelerated features, one can find 
a code for calculating 3- and 4-motifs using VDMC, a distributed algorithm to calculate 3- and 4-motifs in a 
GPU-parallelized way.

## Versions
- Last version: 0.1.44
- Last stable version: 0.1.22

## What Features Can Be Calculated Here?
The set of all vertex features implemented in graph-measures is the following. 
The features that have an accelerated version are written in bold:
* Average neighbor degree
* General (i.e. degree if undirected, else or (in-degree, out-degree))
* Louvain (i.e. implement Louvain community detection method, then associate to each vertex the number of vertices 
in its community)
* Hierarchy energy
* **Motifs**
* **K core**
* **Attraction basin** 
* **Page Rank**
* Fiedler vector
* Closeness centrality
* Eccentricity
* Load centrality
* **BFS moments**
* **Flow** 
* Betweenness centrality
* Communicability betweenness centrality
* Eigenvector centrality
* Clustering coefficient
* Square clustering coefficient
* Generalized degree
* All pairs shortest path length
* All pairs shortest path

Aside from those, there are some other [edge features](https://github.com/AmitKabya/graph-measures/tree/master/src/graphMeasures/features_algorithms/edges).
Some more information regarding the features can be found in the files of [features_meta](https://github.com/AmitKabya/graph-measures/blob/master/src/graphMeasures/features_meta).

## Dependencies
```requirements.txt
setuptools
networkx==2.6.3
pandas
numpy
matplotlib
scipy
scikit-learn
python-louvain
bitstring
future
torch
```

## How To Use The Accelerated Version (CPU/GPU)?
Both versions currently are not supported with the pip installation. \
To use the accelerated version, one must use <b>*Linux* operation system</b> and <b>*Anaconda* distribution</b>, with the follow the next steps:
1. Go to the [package's GitHub website](https://github.com/AmitKabya/graph-measures) and manually download:

   - The directory `graphMeasures`.
   - The python file `runMakefileACC.py`.

   *You might need to download a zip of the repository and extract the necessary files.*
2. Place both the file and the directory inside your project, and run `runMakefileACC.py`.
3. Move to the *boost environment*: `conda activate boost` (The environment was created in step 2).
4. Use the package as explained in the section `How To Use?`

## Installation Through pip
The full functionality of the package is currently available on a Linux machine, with a Conda environment.
- Linux + Conda<br>1. Go to base environment<br>2. If pip is not installed on your env, install it. Then, use pip to install the package
- Otherwise, pip must be installed.
```commandline
pip install graph-measures
```
**Note:** On Linux+Conda the installation might take longer (about 5-10 minuets) due to the compilation of the c++ files.
## How To Use?
Even though one has installed the package as `graph-measures`, The package should be imported from the code as `graphMesaures`. Hence, use:
```python
import graphMeasures
```
## Calculating Features

There are two main methods to calculate features:
1. Using [FeatureCalculator](https://github.com/AmitKabya/graph-measures/blob/master/src/graphMeasures/features_for_any_graph.py) (**recommended**): \
A class for calculating any requested features on a given graph. \
The graph is input to this class as a text-like file of edges, with a comma delimiter, or a networkx _Graph_ object. 
For example, the graph [example_graph.txt](https://github.com/AmitKabya/graph-measures/blob/master/src/graphMeasures/measure_tests/example_graph.txt) is the following file: 
    ```
    0,1
    0,2
    1,3
    3,2
    ```
    Now, an implementation of feature calculations on this graph looks like this:
    ```python
   import os
   from graphMeasures import FeatureCalculator
   # set of features to be calculated
   feats = ["motif3", "louvain"]
   # path to the graph's edgelist or nx.Graph object
   graph = os.path.join("measure_tests", "example_graph.txt")
   # The path in which one would like to save the pickled features calculated in the process. 
   dir_path = "" 
   # More options are shown here. For infomation about them, refer to the file.
   ftr_calc = FeatureCalculator(path, feats, dir_path=dir_path, acc=True, directed=False, gpu=True, device=0, verbose=True)
   # calculate the features. If one do not want the features to be saved,
   # one should set the parameter 'should_dump' to False (set to True by default).
   ftr_calc.calculate_features()
   mx = ftr_calc.feature_matrix
    ``` 
   More information can be found in [features_for_any_graph.py](https://github.com/AmitKabya/graph-measures/blob/master/src/graphMeasures/features_for_any_graph.py). \
   **Note:** If one set `acc=True` without using a Linux+Conda machine, an exception will be thrown.\
   **Note:** If one set `gpu=True` without using a Linux+Conda machine that has cuda available on it, an exception will be thrown.
2. By the calculations as below **(less recommended)**: \
The calculations require an input graph in NetworkX format, later referred as gnx, and a logger.
For this example, we build a gnx and define a logger:
    ```python
   import networkx as nx
   from graphMeasures.loggers import PrintLogger
    
   gnx = nx.DiGraph()  # should be a subclass of Graph
   gnx.add_edges_from([(0, 1), (0, 2), (1, 3), (3, 2)])
    
   logger = PrintLogger("MyLogger")
    ```
    On the gnx we have, we will want to calculate the topological features.
    There are two options to calculate topological features here, depending on the number of features we want to calculate: 
    * Calculate a specific feature:

    ```python
    import numpy as np
    # Import the feature. 
    # If simple, import it from vertices folder, otherwise from accelerated_graph_features: 
    from graphMeasures.features_algorithms.vertices.louvain import LouvainCalculator  
    
    feature = LouvainCalculator(gnx, logger=logger)  
    feature.build()  # The building happens here
    
    mx = feature.to_matrix(mtype=np.matrix)  # After building, one can request to get features the a matrix 
    ```

    * Calculate a set of features (one feature can as well be calculated as written here):

    ```python
   import numpy as np
   from graphMeasures.features_infra.graph_features import GraphFeatures
   from graphMeasures.features_infra.feature_calculators import FeatureMeta
   from graphMeasures.features_algorithms.vertices.louvain import LouvainCalculator
   from graphMeasures.features_algorithms.vertices.betweenness_centrality import BetweennessCentralityCalculator
    
   features_meta = {
       "louvain": FeatureMeta(LouvainCalculator, {"lov"}),
       "betweenness_centrality": FeatureMeta(BetweennessCentralityCalculator, {"betweenness"}),
   }  # Hold the set of features as written here. 
    
   features = GraphFeatures(gnx, features_meta, logger=logger) 
   features.build()
    
   mx = features.to_matrix(mtype=np.matrix)
    ```
   
   **Note:** All the keys-values options that can be set in the `features_meta` variable can be found
   in `graphMeasures.features_meta` or `graphMeasures.accelerated_features_meta`
   ```python
   from graphMeasures.features_meta import FeaturesMeta
   # if one uses the accelerated calculation:
   # from graphMeasures.accelerated_features_meta import FeaturesMeta
   all_possible_features_meta = FeaturesMeta().NODE_LEVEL
   
   # all possible features
   print(all_possible_features_meta.keys())   
   # get the value for louvain
   louvain = all_possible_features_meta['louvain']   
   # get the value for betweenness_centrality
   betweenness_centrality = all_possible_features_meta['betweenness_centrality']
   ```
