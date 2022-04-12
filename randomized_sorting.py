from math import ceil
import random
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

#Reading excel files 
preferences_file= pd.read_excel("preferences.xlsx")
nuid_file= pd.read_excel("NUID.xlsx")

#Merging the rastor file (NUID.xlsx) and preferences file
merge = preferences_file.loc[:, 'Email' : 'last_project'].merge(nuid_file[["NUID","Email"]], left_on='Email', right_on = "Email", how='left')

#Sending merged files into an a single excel file called Result.xlsx
merge.to_excel("Results.xlsx", index = False)

#Reading merged file (Result.xlsx)
merged_files = pd.read_excel("Results.xlsx", index_col=False)

#Sending data from merged excel files to Pandas Database
mer_df = pd.DataFrame(merged_files)  

#Creating list of NUIDs 
nuid_list_t = mer_df.loc[1:,'NUID'].values.tolist()
random.shuffle(nuid_list_t)

#calculating number of projects
row_num = (mer_df.shape[0] - 1)
col_num = len(mer_df.loc[: ,'project1' : 'last_project'].columns)
num_stu_t = ceil(row_num / col_num)

#Determining first and second year students
sy_stu = mer_df.loc[(mer_df['academic_year'] == 'Senior') & (mer_df['academic_program'] == 'Software Engineering')]
fy_stu = mer_df.loc[((mer_df['academic_year'] == 'Senior') & (mer_df['academic_program'] != 'Software Engineering')) | (mer_df['academic_year'] == 'Junior')]

#Creating list of nuids for fy-students and sy-students and randomizing the lists
nuid_list_fy = fy_stu.loc[1:,'NUID'].values.tolist()
random.shuffle(nuid_list_fy)
nuid_list_sy = sy_stu.loc[1:,'NUID'].values.tolist()
random.shuffle(nuid_list_sy)

#Calculating number of first year and second year students
row_num_fy = (fy_stu.shape[0])
col_num_fy = len(fy_stu.loc[: ,'project1' : 'last_project'].columns)
num_stu_fy = ceil(row_num_fy/ col_num_fy)

row_num_sy = (sy_stu.shape[0])
col_num_sy = len(sy_stu.loc[: ,'project1' : 'last_project'].columns)
num_stu_sy = ceil(row_num_sy/ col_num_sy)

#Creating dictionaries to store first and second year students together with their assigned projects
fys_dict = {'project':[], 'first_name':[], 'last_name':[], 'NUID':[], 'preference':[]}
sys_dict = {'project':[], 'first_name':[], 'last_name':[], 'NUID':[], 'preference':[]}

#Defining a function to automatically sort students based on which list of NUID they are in, the max number of students/project, 
#and their respective dictionary
def sortStudents(nuid_list, num_stu, s_dict):

    for nuid in nuid_list:

        #Select row where nuid lies
        selected_row = mer_df.loc[mer_df['NUID'] == nuid]

        #Creating variables for first name and last name
        first_name = selected_row['first_name'].to_string(index=False)
        last_name = selected_row['last_name'].to_string(index=False)

        #Only selecting project columns and preferences row where NUID lies
        p_in_sr = selected_row.iloc[: , -(col_num+1) : -1]

        #Making a list of preferences
        pref_list = p_in_sr.values.flatten().tolist()    
        pref_lst = [int(pr_l) for pr_l in pref_list]

        

        #Labeling minimum preference from pref_list as min_pref        
        min_pref = min(pref_lst)

        while min_pref >= 0:   
            
            #Creating a project number list [project1, project2, ...]
            project_df = mer_df.iloc[:, - (col_num+1) : -1]
            project_num_list = project_df.columns.values.tolist()
            project_num_lst = [str(y) for y in project_num_list]

            #Creating a list of project names 
            p_name_list = project_df.iloc[0,:].values.tolist()
            p_name_lst = [str(z) for z in p_name_list]

            #Making a dataframe which can be used to find project name with min_pref
            t_df = pd.DataFrame(list(zip(p_name_lst,project_num_lst, pref_lst)), columns= ['projects', 'project_num','preferences'])
            t_df['preferences'] - 1      
        
            #Select project name where min_pref lies
            projects_row = t_df.loc[t_df['preferences'] == min_pref]
            p_name = projects_row['projects'].to_string(index=False)

            #Calculating the number of times the selected project was inserted in dictionary new_row
            project_in_new_row = s_dict['project']
            amt_p_name = project_in_new_row.count(p_name)

            #If the amount of students in a project has not reached the max amount, add them to their respective dictionary                       
            if amt_p_name < num_stu:
                s_dict['project'].append(p_name)
                s_dict['first_name'].append(first_name)
                s_dict['last_name'].append(last_name)
                s_dict['NUID'].append(nuid)
                s_dict['preference'].append(min_pref)
                yield s_dict
                break   
            #Else min_pref is now the next smallest preference
            else:
                min_pref += 1

#Creating a function to convert the results obtained from sortStudents into a dataframe
def createDf(id_lst, num_st, st_dict): 
    for fystu in sortStudents(id_lst,num_st, st_dict):
        fy_stu = fystu
    fys_df = pd.DataFrame(fy_stu)    
    return fys_df

#Sorting the first and second year students and assigning them to their repective dataframes
sorted_SYS_df = createDf(nuid_list_sy, num_stu_sy,sys_dict)
sorted_FYS_df = createDf(nuid_list_fy, num_stu_fy,fys_dict)

#Combining the first and second year student dataframes
lst = [sorted_SYS_df, sorted_FYS_df]
combined_sorted_df = pd.concat(lst)

#Sorting the resulting dataframe 
sorted_df = combined_sorted_df.sort_values(by='project')

#Sending the sorted dataframe to excel
sorted_df.to_excel('output.xlsx', index=False)
print(sorted_df)


#Plotting bar graph for preferences
fig = plt.figure(figsize =(10, 7))
df = sorted_df.groupby(['preference']).size().reset_index(name='count')
print(df)

plt.bar(df['preference'], df['count'], color ='maroon',
        width = 0.75)
 
plt.xlabel("Preferences")
plt.ylabel("No. of students")
plt.title("Preferences Obtained By Students")
plt.show()






  


    
