**EduNet resource recommendation class**
----------
* Introduction
This resource recommendation class suggests the 5 most appropriate sources for self-learning either in the form of pdf files or youtube video links, based on the weak knowledge points of the student and the KPs provided by the sources.

* Input format
class Prototype1_final.get_resource_recommendations(weak_KP=None))

* Additional reuirements:
Make sure you have downloaded utils from UPA on Gitlab: 
https://gitlab.com/fillantrophy02/edunet/-/tree/main/UPA/utils

* Input parameters:
weak_KPs: list of strings, default=none
List of weak knowledge points of the student

* Parameters:

* Attributes
get_resource_recommendations: json
5 recommended resources in json format: [{"title":string,"kp_available": list of strings,"section":string}]

Example: 
File Prototype1_final.py



