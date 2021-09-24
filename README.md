# FrameExtractionMammogram
A hybrid information extraction system for unstructured mammography reports.  
• Generates information frames using dependency parsing and distributed semantics.  
• Information frames comprise entities and relations that capture imaging observations.  
• This system obtains a F1-score of 0.94 in extracting complete lesion information.  
• Outperforms a state-of-the-art rule-based system in generating complete information.



1. bigrams.py - To obtain word vectors from the mammography reports.
2. kmeans.py - Applying kmeans to the word vectors.
3. elbow.py - Creating an elbow plot for vectors.
4. dependency_all_core.py - Extracting dependency relations from reports.
5. extract_relations_core_3.py - To extract relations from reports


Citation: Gupta, Anupama, Imon Banerjee, and Daniel L. Rubin. "Automatic information extraction from unstructured mammography reports using distributed semantics." Journal of biomedical informatics 78 (2018): 78-86.
