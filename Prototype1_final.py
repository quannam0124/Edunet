import pandas as pd
import numpy as np
import operator
from operator import itemgetter
import urllib.parse
import urllib.request
import json, os, re
from utils import load_from_mongodb

class ResourceRecommendation:
    def __init__(self):
        self.list_of_KPs = self.load_KPs()
        self.list_of_resources = self.load_resources()



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
            id = doc.get('tree_id')
            list_of_KPs.append(id)
            
        return list_of_KPs
    
    def load_KP_names(self):
        list_of_KP_names = []
        r_exp = '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\.[0-9]$'
        queries = {'tree_id': {'$regex': r_exp}}
        detail = {'tree_id': 1, 'name': 1}
        results = load_from_mongodb('edunet', 'students_kp', queries, detail)
        for docs in results:
            list_of_KP_names.append(docs.get('name'))
        return list_of_KP_names

    def load_KPs_for_FS1(self):
        """Load all available Knowledge Points from Database
        
        Parameters
        ----------
        N.A.

        Returns
        -------
        list of strings
            A list of all KPs available in the database
        """
        list_of_KPs_1 = []
        r_exp = '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\.[0-9]$'
        query = {'tree_id': {'$regex': r_exp}}
        details = {'tree_id': 1, 'name': 1}
        result = load_from_mongodb('edunet', 'students_kp', query, details)
        for doc in result:
            id = doc.get('tree_id')
            name = doc.get('name')
            list_of_KPs_1.append((id, name))
            
        return list_of_KPs_1


    def load_resources(self):
        """Load all available resources from API
        
        Parameters
        ----------
        N.A.

        Returns
        -------
        pandas DataFrame
            (need description of the returns)
        """
        query = {}
        details = {"tree_id" : 0}
        Resources = load_from_mongodb('tracie', 'resource_kp', query, details)

        resource_info = []
        resource_id = []
        for resource in Resources:
            resource_id.append(resource.get('_id'))
            resource_info.append([resource.get('title'),  resource.get('kp_available'), resource.get('url'), resource.get('section')])
        resources_metadata = pd.DataFrame(columns = ['title', 'kp_available', 'url', 'section'], index = resource_id, data = resource_info)
            
        return resources_metadata

    def retrieve_StudentVector(self, weak_KP):
        Student_vector = []
        for knowledge_point in self.list_of_KPs:
            if knowledge_point in weak_KP:
                Student_vector.append(1)
            else:
                Student_vector.append(0)
        return Student_vector

    def retrieve_ResourceVector(self, resource_id):
        Resource_vector = []
        Resource_database = self.list_of_resources
        KP_contained = Resource_database.at[resource_id, 'kp_available']
        for knowledge_point in self.list_of_KPs:
            if knowledge_point in KP_contained:
                Resource_vector.append(1)
            else:
                Resource_vector.append(0)
        return Resource_vector

     #calculate similarity score    
    
    def cosine_sim(self, Student, Resource):
        dot = sum(a*b for a, b in zip(Student, Resource))
        #norm_a = sum(a*a for a in Student) ** 0.5
        #norm_b = sum(b*b for b in Resource) ** 0.5
        #cos_sim = dot / (norm_a*norm_b)
        return dot

    def get_resource_recommendations(self, weak_KP):
        """Get recommended resources for a particular student
        Parameters
        -------
        weak_KP: KPs that a student needs to learn

        Returns
        -----
        List of top 5 recommended resources for the student"""
        #Retrieve student vector
        Student_vector = self.retrieve_StudentVector(weak_KP)
        #Retrieve resource metadata
        Resource_database = self.load_resources()       

        def get_recommendations():
            recommended_resource_pddf = pd.DataFrame(columns = ['id', 'title', 'KP_available', 'URL', 'Page number'])
            Similarity_score = []
            recommendations = []
            for i in Resource_database.index:
                resource_vector = self.retrieve_ResourceVector(i)
                score = self.cosine_sim(Student_vector, resource_vector)
                Similarity_score.append((i, score))
            sorted_score = sorted(Similarity_score, key = itemgetter(1), reverse = True)
            for resource_id in sorted_score[0:10]:
                #recommendations.append((resource_id[0]))
            #recommended_resource_pddf = self.list_of_resources.loc[recommendations, :]
                recommendations.append([resource_id[0], Resource_database.at[resource_id[0], 'title'], Resource_database.at[resource_id[0], 'kp_available'], Resource_database.at[resource_id[0], 'url']])
                #recommendations_df.iloc[i, :] = recommendations 
            #recommendations_json = recommended_resource_pddf.to_json(orient = "records")
            return recommendations
        return get_recommendations()


  