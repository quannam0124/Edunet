import pandas as pd
import json, os
from Prototype1_final import ResourceRecommendation

obj = ResourceRecommendation()
weak_KP = ['1.7.1.1.1', '1.8.1.1.1', '1.9.1.1.1']


print(obj.get_resource_recommendations(weak_KP))