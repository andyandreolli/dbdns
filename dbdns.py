import json
import numpy as np
import matplotlib.pyplot as plt



def load(fpath,**kwargs):
# Returns the whole database as a dictionary or, if optional argument sim is passed,
# the sub-dictionary associated to the requested simulation. Syntax:
# dictionary = load('path/to/db.toml', sim='simulation_id')

    sim = kwargs.get('sim', None)

    with open(fpath) as infile:
        db = json.load(infile)
    if sim:
        db = db[sim]

    return db



def save(d2s,fpath,**kwargs):
# Write dns database to disk. A dictionary is passed to this function;
# if the dictionary represents the whole database (no 'sim' optional argument),
# the whole dictionary is written to disk. Otherwise, only the specified simulation
# is added to the dictionary written on disk. Syntax:
# save(dictionary_to_save, 'path/to/db.toml', sim='simulation_id')

    sim = kwargs.get('sim', None)

    d2s = fix_dictionary(d2s) # clean up the dictionary before saving

    if sim: # if only one simulation needs to be saved
        fulldb = load(fpath) # load full database
        fulldb[sim] = d2s # apply changes
        with open(fpath, 'w') as outfile: 
            json.dump(fulldb, outfile, indent=4)
    else: # save whole dictonary
        if full_db_check(d2s):
            with open(fpath, 'w') as outfile: 
                json.dump(d2s, outfile, indent=4)
        else:
            raise Exception('The dictionary provided is not a full database, but possibly a single simulation; this because it contains items that are not dictionaries themselves.')



def fix_dictionary(dct):
# Recursive function that cleans up a dictionary.
# To be used before saving to database. Syntax:
# dictionary = fix_dictionary(dictionary)

    todelete = []

    for item in dct:
        if dct[item] == None: # add empty items to list of items to delete
            todelete.append(item)
        elif isinstance(dct[item], (list, tuple, np.ndarray)): # list are not allowed; only first element is kept
            dct[item] = dct[item].iat[0]
        elif type(dct[item]) is dict: # if an element is a dictionary, function is called recursively
            dct[item] = fix_dictionary(dct[item])
        if isinstance(dct[item], (np.ndarray, np.generic)): # numpy datatypes are casted to standard types
            dct[item] = dct[item].item()
        

    for delit in todelete: # delete unwanted items
        dct.pop(delit)

    return dct



def full_db_check(dct):
# To be run when writing a full database; checks that
# all items of dictionary are dictionaries themselves.
# If this is not verified, the dictionary is surely not
# a full database.

    is_full = True

    for item in dct:
        if type(dct[item]) is not dict:
            is_full = False
            break
    
    return is_full



def dict_list(dct,tpl):
# Accesses elements of a dictionary with list indexing
    if not isinstance(tpl,list):
        tpl = [tpl]
    if len(tpl) == 1:
        return dct[tpl[0]]
    elif len(tpl) == 2:
        return dct[tpl[0]][tpl[1]]
    else:
        raise Exception('Three-times-nested dictionaries are not yet supported; please pass a tuple of maximum length 2.')



class dbplot:

    def __init__(self,fpath,settingspath):
        self.database = load(fpath)
        with open(settingspath) as stngs:
            self.settings = json.load(stngs)

    def plot(self,x,y,**kwargs):
        factor = kwargs.get('factor',1)
        fig, ax = plt.subplots()
        for sim in self.database:
            sdb = self.database[sim]
            try:
                dataset = sdb['meta']['dataset']
            except:
                dataset = 'mine'
            try:
                xval = dict_list(sdb,x)
                yval = dict_list(sdb,y)
                if sdb['meta']['problem'] == 'cou':
                    xval *= factor
                ax.scatter(xval, yval, marker=self.settings['datasets'][dataset]['shape'], color=self.settings['problems'][sdb['meta']['problem']])
            except Exception as message:
                if x == 'rew' or y == 'rew':
                    x = x.replace('rew', 'reb')
                    y = y.replace('rew', 'reb')
                    xval = dict_list(sdb,x)
                    yval = dict_list(sdb,y)
                    if sdb['meta']['problem'] == 'cou':
                        xval *= factor
                    ax.scatter(xval, yval, marker=self.settings['datasets'][dataset]['shape'], color=self.settings['problems'][sdb['meta']['problem']])
                elif x == 'reb' or y == 'reb':
                    x = x.replace('reb', 'rew')
                    y = y.replace('reb', 'rew')
                    xval = dict_list(sdb,x)
                    yval = dict_list(sdb,y)
                    if sdb['meta']['problem'] == 'cou':
                        xval *= factor
                    ax.scatter(xval, yval, marker=self.settings['datasets'][dataset]['shape'], color=self.settings['problems'][sdb['meta']['problem']])
                else:
                    print('Error with simulation', sim)
                    print(message)
        plt.show()

    def printout(self,x,y,**kwargs):
        lines = ''
        for sim in self.database:
            sdb = self.database[sim]
            try:
                dataset = sdb['meta']['dataset']
            except:
                dataset = 'mine'
            try:
                xval = dict_list(sdb,x)
                yval = dict_list(sdb,y)
                lines += sdb['meta']['problem'] + '\t' + dataset + '\t\t' + "{:20}".format(xval) + '\t' + "{:20}".format(yval) + '\n'
            except Exception as message:
                if len(x) == 1:
                    x = x[0]
                if len(y) == 1:
                    y = y[0]
                if 'rew' in x or 'rew' in y:
                    x = x.replace('rew', 'reb')
                    y = y.replace('rew', 'reb')
                    xval = dict_list(sdb,x)
                    yval = dict_list(sdb,y)
                    lines += sdb['meta']['problem'] + '\t' + dataset + '\t\t' + "{:20}".format(xval) + '\t' + "{:20}".format(yval) + '\n'
                elif 'reb' in x or 'reb' in y:
                    x = x.replace('reb', 'rew')
                    y = y.replace('reb', 'rew')
                    xval = dict_list(sdb,x)
                    yval = dict_list(sdb,y)
                    lines += sdb['meta']['problem'] + '\t' + dataset + '\t\t' + "{:20}".format(xval) + '\t' + "{:20}".format(yval) + '\n'
                else:
                    print('Error with simulation', sim)
                    print(message)
        print()
        print('\n'.join(sorted(lines.splitlines())))
        print()
