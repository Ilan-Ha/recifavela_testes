# import the modules
# os.path.join(mydir, myfile)
# ou
# pathlib.Path(mydir, myfile)
# ou 
# pathlib.Path(mydir) / myfile
# # os.path.join( "C:", "meshes", "as" )
import os
from os import listdir
import pandas as pd
import shutil

csvs = os.path.join(os.getcwd(),'csv')
pwd = os.path.join(os.getcwd(),'images','temp')
main_path = os.path.join("images","datasets","joebeachcapital","realwaste","versions","1","realwaste-main","RealWaste")
to_change = []
csv_name = 'realwaste.csv'
# print(main_path)
def copy_images():
    # essa função serve para facilitar analisar imagem por imagem para decidir qual são pet
    f_name = 'Plastic'
    current_path = os.path.join(main_path,f_name)
    folder = os.path.join(pwd,f_name)
    x = 0
    y = 1
    fold = os.path.join(folder,str(y))
    for image in os.listdir(current_path):
        if x >= 10:
            x = 0
            y = y + 1
            fold = os.path.join(folder,str(y))
        if not os.path.exists(fold):
            os.makedirs(fold)
        ipath = os.path.join(current_path,image)
        shutil.copy(ipath,fold)
        x = x + 1

def cvv_creator():
    folders = []
    for folder in os.listdir(main_path):
        folders.append(folder)

    # print(folders)

    # get the path/directory
    # folder_dir = "images\\datasets\\joebeachcapital\\realwaste\\versions\\1\\realwaste-main\\RealWaste\\Cardboard"
    # for images in os.listdir(folder_dir):

    #     # check if the image ends with png
    #     if (images.endswith(".jpg")):
    #         print(images)

    # path  label
    ipath = []
    lbl = []
    group = []
    for folder in folders:
        current_path = os.path.join(main_path,folder)
        for image in os.listdir(current_path):
            if(image.endswith(".jpg")):
                file_path = os.path.join(current_path,image)
                ipath.append(file_path)
                lbl.append(folder.lower())
                group.append(-1)

    data = {'image_path':ipath,'label':lbl,'group':group}
    df = pd.DataFrame(data)

    c_folder = os.path.join(csvs,'created')
    if not os.path.exists(c_folder):
            os.makedirs(c_folder)

    df.to_csv(os.path.join(c_folder,csv_name),index=True,index_label='id')

def update_cvv():
    i_path = os.path.join(main_path,'Plastic')
    df = pd.read_csv(os.path.join(csvs,'created',csv_name))
    for image in to_change:
        c = os.path.join(main_path,'Plastic','Plastic_'+image+'.jpg')
        #print(c)
        #d = df[df["image_path"]==c]
        #print(d.index)
        #print(d)
        #print(df)
        #print(df.loc[0])
        #result = df.loc[:,'id']
        #print(result)
        result = df.loc[df['image_path']==c,'id'].values[0]
        print(result)
        df.loc[result,'label'] = 'pet'
    c_folder = os.path.join(csvs,'images')
    df.to_csv(os.path.join(c_folder,csv_name),index=False)

def manual_cvv():
    f_name:list = []
    f_group: list = []
    x = 0
    for (root,dirs,files) in os.walk(os.path.join(pwd,"mesmos_objetos"),topdown=True):
        # print("Directory path: %s"%root)
        # print(f"Directory Names: {dirs}\tis empty? {bool(dirs)}")
        # print(f"Files Names: {files}\tis empty? {bool(files)}")
        if files:
            for file in files:
                f_name.append(file)
                f_group.append(x)
            x = x + 1
    
    data = {'image_name':f_name,'group':f_group}
    df = pd.DataFrame(data)
    
    c_folder = os.path.join(csvs,'images')
    if not os.path.exists(c_folder):
                os.makedirs(c_folder)
    
    df.to_csv(os.path.join(c_folder,"realwates_groups.csv"),index=True,index_label='id')
    
def cvv_temp():
    images = []
    group = []
    f_name = []
    group_count = 0
    # 'Textile Trash'
    # 'Plastic'
    directory = os.path.join(pwd,'Plastic','objetos')
    for (root,dirs,files) in os.walk(directory,topdown=True):
        # print("Directory path: %s"%root)
        # print("Directory Names: %s"%dirs)
        # print("Files Names: %s"%files)
        if files:
            # refazer
            folder_name = os.path.relpath(root,directory)
            # path lib -> .relative_to()
            #folder_name = root.removeprefix(directory)
            for file in files:
                images.append(file)
                group.append(group_count)
                f_name.append(folder_name)
            group_count = group_count + 1
    data = {'image':images,'folder':f_name,'group':group}
    df = pd.DataFrame(data)
    # plastic
    # textileTrash
    df.to_csv(os.path.join(csvs,'groups','realwaste_plastic_groups.csv'),index=True,index_label='id')

def temp_fun():
    dg = pd.read_csv(os.path.join(csvs,'created',csv_name))
    dpl = pd.read_csv(os.path.join(csvs,'groups','realwaste_plastic_groups.csv'))
    dtt = pd.read_csv(os.path.join(csvs,'groups','realwaste_textileTrash_groups.csv'))
    for index in range(len(dpl)):
        path = os.path.join(main_path,'Plastic',dpl.loc[index,'image'])
        id = dg[dg['image_path']==path].iloc[-1]['id']
        # print(f"{'-'*20}\n{id}")
        # tem_1 = dg.loc[id,'group']
        # print(f"\t{type(tem_1)}\n{tem_1}")
        # tem_2 = dpl.loc[index,'group']
        # print(f"\t{type(tem_2)}\n{tem_2}")

        dg.loc[id,'group'] = dpl.loc[index,'group']

    result = dpl.iloc[-1]['group']
    x = result + 1
    for index in range(len(dtt)):
        path = os.path.join(main_path,'Textile Trash',dtt.loc[index,'image'])
        id = dg[dg['image_path']==path].iloc[-1]['id']

        dg.loc[id,'group'] = dtt.loc[index,'group'] + x

    # x = result + 1
    # no_group = dg[dg['group']==-1]
    # i_group = dg[dg['group']!=-1]
    # ids = no_group['id'].values
    # for index in range(len(ids)):
    #     # print(no_group.loc[ids[index]]['image_path'])
    #     path = no_group.loc[ids[index]]['image_path']
    #     id = dg[dg['image_path']==path].iloc[-1]['id']
    #     dg.loc[id,'group'] = x
    #     x = x + 1

    c_folder = os.path.join(csvs,'created')
    dg.to_csv(os.path.join(c_folder,csv_name),index=False)
    # no_group.to_csv(os.path.join(c_folder,"no_group.csv"),index=False)
    # i_group.to_csv(os.path.join(c_folder,"i_group.csv"),index=False)

def creator():
    df = pd.read_csv(os.path.join(csvs,'groups','realwaste_textileTrash_groups.csv'))
    current_path = os.path.join(main_path,"Textile Trash")
    folder = os.path.join(pwd,"Textile Trash")
    x = 0
    y = 1
    fold = os.path.join(folder,str(y))
    for image in os.listdir(current_path):
        d_temp = df[df['image']==image]
        if not d_temp.empty :
            temp = d_temp.iloc[-1]['folder']
            temp = os.path.split(temp)
            working = ''
            for item in temp:
                working = os.path.join(working,item)
                # o erro é que começa com \
                # print(working)
            # print(working)
            #working = working.removeprefix('\\')
            fold = os.path.join(folder,'objetos',working)
            #print(os.path.join(pwd,working))
        else:    
            fold = os.path.join(folder,'images',str(y))
            if x >= 10:
                x = 0
                y = y + 1
            x = x + 1
        if not os.path.exists(fold):
            os.makedirs(fold)
        ipath = os.path.join(current_path,image)
        shutil.copy(ipath,fold)

# creator()
#copy_images()

cvv_creator()
temp_fun()

#update_cvv()
#manual_cvv()
# cvv_temp()
# df = pd.read_csv(os.path.join(csvs,'images','realwates_groups.csv'))
# result = df.iloc[-1]['group']
# x = result + 1
# dg = pd.read_csv(os.path.join(csvs,'images',csv_name))
# h = dg.loc[:,'image_path']
# # files: list = []
# # for serie in h:
# #      files.append(os.path.basename(os.path.normpath(serie)))
# dg['group'] = x 
# images = df.loc[:,'image_name':'group']
# for image in images.iterrows():
#     print(image)



