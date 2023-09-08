

#obj = ResourceRecommendation()
#weak_KP = ['1.9.1.1.5', '1.9.1.1.6', '1.9.1.1.7', '1.9.1.1.8', '1.9.1.1.9']



#obj = ResourceRecommendation()
#list_of_KPs = obj.load_KPs()
#KP_List = list_of_KPs
#list_of_names = obj.load_KP_names()
#KP_names = list_of_names
#KP_metadata = pd.DataFrame(columns = ['KP_name'], index = KP_List, data = KP_names)
#KP_metadata.to_excel(r'C:\Users\Admin\Desktop\Assignments\Work stuffs\lop_8.csv')
#print(KP_metadata)


#df = pd.read_csv(r'C:\Users\Admin\Desktop\Assignments\Work stuffs\lop_6_hinh.csv')
#for row in df.index:
#  df.drop(df.index[(df["KP_available"] == '[]')], axis = 0, inplace = True)
#  if df.loc[row, 'KP_available'] == '[]' :
#    df.drop(labels = row, axis = 0)
  #df.to_csv(r'C:\Users\Admin\Desktop\Assignments\Work stuffs\lop6_1.csv')

nums =[2,7,11,15]
target = 9
result=[]
for a in range(len(nums)): 
    if target-nums[a] in nums and target-nums[a]!=nums[a]:
        result.append(a)
        result.append(nums.index(target-nums[a])
    return result
print(result)
