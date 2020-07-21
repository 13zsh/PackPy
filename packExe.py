import sys
import os
import os.path
import time
import copy
from shutil import copyfile


def getfiles(filepath):
    g = os.walk(filepath)
    filelist = list()
    for path, dir_list, file_list in g:
        for file_name in file_list:
            filelist.append(os.path.join(path, file_name))
    return filelist


def getfolders(filepath):
    g = os.walk(filepath)
    folderlist = list()
    for path, dir_list, file_list in g:
        for dir_name in dir_list:
            folderlist.append(os.path.join(path, dir_name))
    return folderlist


def getignore(filename):
    a = open(filename)
    lines = a.readlines()
    for i in lines:
        itemp = i.strip()
        if itemp in ['\n', '\r\n']:
            lines.remove(i)
    return lines


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)


def copyfiles(source, target, sourcefolder='Release'):
    for filepath in source:
        index = filepath.index(sourcefolder) + len(sourcefolder) + 1
        #filename = os.path.basename(filepath) 获取路径的文件名称
        filename = filepath[index:]
        targetpath = target + '\\' + filename
        try:
            copyfile(filepath, targetpath)
        except IOError as e:
            print("Unable to copy file. %s" % e)
        except:
            print("Unexpected error:", sys.exc_info())


def creatfolders(where, folders, sourcefolder='Release'):
    for filepath in folders:
        index = filepath.index(sourcefolder) + len(sourcefolder) + 1
        folder = filepath[index:]
        #folder = filepath.split("\\")[-1] 获取路径下的最后的文件夹名称
        mkdir(where + '\\' + folder)


def getreleasefolder():
    #return os.path.abspath(os.path.dirname(os.getcwd())) + '\\Release' + '\\' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) 取得上一级目录的Release + 时间
    return os.getcwd() + '\\' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

def removefolders(folders, rules):
    if (len(folders) == 0): return
    if (len(rules) == 0): return folders
    purefolders = copy.deepcopy(folders)
    for folder in folders:
        foldersplit = folder.split('\\')
        for rule in rules:
            purerule = rule.strip().strip('\n')
            if purerule.endswith('/'):
                purerl = purerule.strip('/')
                if purerl in foldersplit:
                    purefolders.remove(folder)
                    break
            else:
                continue
    return purefolders


def removefiles(filepaths, rules):
    if (len(filepaths) == 0): return
    if (len(rules) == 0): return filepaths
    purefilepaths = copy.deepcopy(filepaths)
    for filepath in filepaths:
        filename = os.path.basename(filepath)
        for rule in rules:
            purerule = rule.strip().strip('\n')
            if not purerule.endswith('/'):
                if (purerule[0] == '*') and ('.' in purerule) and (not purerule.endswith('*')):
                    if os.path.splitext(filepath)[-1] == purerule[1:]:
                        purefilepaths.remove(filepath)
                    else:
                        continue
                elif (purerule[0] == '*') and ('.' not in purerule) and (purerule.endswith('*')):
                    nostarrule = purerule.strip('*')
                    if nostarrule in filename:
                        purefilepaths.remove(filepath)
                    else:
                        continue
                else:
                    if filename == purerule:
                        purefilepaths.remove(filepath)
                    else:
                        continue
            else:
                continue
    return purefilepaths


if __name__ == "__main__":
    filecfg = "cfg.txt"
    ignorelist = getignore(filecfg)
    if len(ignorelist) < 2:
        raise Exception("配置文件cfg.txt 格式有误!")
    filepath = ignorelist[0].strip().strip('\n')
    sourcefolder = os.path.split(filepath)[1]

    if len(ignorelist) > 1:
        releasepath = getreleasefolder()
        mkdir(releasepath)
        filelist = getfiles(filepath)
        folderlist = getfolders(filepath)
        del (ignorelist[0])  # 删除第一行路径
        purefolders = removefolders(folderlist, ignorelist)
        purefiles = removefolders(filelist, ignorelist)
        filenames = removefiles(purefiles, ignorelist)
        creatfolders(releasepath, purefolders)
        copyfiles(filenames, releasepath, sourcefolder)
