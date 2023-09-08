import pandas as pd
import numpy as np
import operator
from operator import itemgetter
import urllib.parse
import urllib.request
import re


class ResourceRecommendation:
#Knowledge gaps
database = pd.read_csv(r'C:\Users\nguyennamminhquan\Desktop\Assignments\Work stuffs\UPA\UPA\database\DummyStudentKP.csv', index_col = 0)
#Available resource URL
resources = pd.read_csv(r'C:\Users\nguyennamminhquan\Desktop\Assignments\Work stuffs\UPA\UPA\database\DummyResourcesKP.csv', index_col=0)
#All KP available
#KP_available = pd.read_csv('/content/gdrive/My Drive/Area4L.csv')


##KPlist
KP_List = ['1.9.1.1.1.1', '1.9.1.1.1.2', '1.9.1.1.2.1', '1.9.1.1.3.1', '1.9.1.1.3.2', '1.9.1.1.3.3', '1.9.1.1.4.1','1.9.2.1.1.1', '1.9.2.2.1.1', '1.9.2.2.2.2', '1.9.2.2.2.3', '1.9.2.2.2.4', '1.9.2.2.2.5', '1.9.2.2.3.1', '1.9.3.1.1.1', '1.9.3.1.2.1', '1.9.3.2.1.1']
def load_KPs(self):
        """Load all available Knowledge Points from Database
        
        Parameters
        ----------
        N.A.

        Returns
        -------
        list of strings
            A list of all KPs available in the database
        """
        list_of_KPs = []
        r_exp = '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\.[0-9]$'
        query = {'tree_id': {'$regex': r_exp}}
        details = {'tree_id': 1}
        result = load_from_mongodb('edunet', 'students_kp', query, details)
        for doc in result:
            list_of_KPs.append(doc.get('tree_id'))

        return list_of_KPs


0

def retrieve_StudentVector(ID, datafile, column):
    Vector = []
    Weak_KP = datafile.at[ID,column] 
    for a in (KP_List):
      if a in (Weak_KP):
        Vector.append(1)
      else:
        Vector.append(0)
    return Vector

def retrieve_ResourceVector(ID2, datafile2, column2):
    Vector2 = []
    Contained_KP = datafile2.at[ID2, column2]
    for a in (KP_List):
      if a in (Contained_KP):
        Vector2.append(1)
      else:
        Vector2.append(0)
    return Vector2


def cosine_sim(Student, Resource):
    dot = sum(a*b for a, b in zip(Student, Resource))
    norm_a = sum(a*a for a in Student) ** 0.5
    norm_b = sum(b*b for b in Resource) ** 0.5
    cos_sim = dot / (norm_a*norm_b)
    return dot
    
df3 = pd.DataFrame(columns = resources.columns, index = [database.index])
  #print(df3.head())

def similarity(student, resource):
    similarity_index = cosine_sim(retrieve_StudentVector(student, database, 'KP'), 
            retrieve_ResourceVector(resource, resources, 'KP_contained'))
    return similarity_index



def add_score(i):
    score = []
    for resource in resources.index:
      score.append((resource, (similarity(i, resource))))
    sorted_list = sorted(score, key = itemgetter(1), reverse = True)
    #return sorted_list[0:5]
    recommendations = []
    for i in sorted_list[:3]:
      recommendations.append(resources.loc[i[0], :])
    return recommendations
    #res_list = [i[0] for i in sorted_list[0:5]]
    #return res_list

print(add_score('9cc30656-f7fe-4222-881c-8e78d7f75c1b'))




  