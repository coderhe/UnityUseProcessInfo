# coding=utf-8
import os
import shutil
import paramiko
import sys
import UEDebug
import svn_cmd
import pysvn

GlobalSlash = "/"


def UploadFiles(localFullPathFileList, remoteDir, userName="uekehuduan", password="uekehuduan", ip="192.168.1.208",
                port=22):
    UEDebug.LogWithLine("-----------Start UploadFiles, The number of uploads is " + str(len(localFullPathFileList)))
    if len(localFullPathFileList) == 0:
        return False
    ssh = None
    sftp = None
    try:
        # 创建ftp连接
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port, userName, password)
        sftp = ssh.open_sftp()
        # 先进入到这个ftp的目录中
        sftp.chdir("/export/ext/samba/")
        # 执行ftp上传操作
        return _DoUploadFiles(sftp, localFullPathFileList, remoteDir)
    except Exception as e:
        UEDebug.LogException(e)
        UEDebug.LogWithLine("-----------UploadFiles error !")
        return False
    finally:
        # 释放ftp
        if sftp:
            sftp.close()
        if ssh:
            ssh.close()
        UEDebug.LogNormal("-----------End UploadFiles")

def _DoUploadFiles(sftp, localFullPathFileList, remoteDir):
    # 创建目标路径所在的文件目录
    _CreateDirFolders(sftp, remoteDir)
    # 复制文件到目标目录
    for localFile in localFullPathFileList:
        if not os.path.exists(localFile):
            UEDebug.LogException("-----------the local file does not exist! dir = " + localFile)
            return False

        fileName = os.path.split(localFile)[1]
        if os.path.isfile(localFile):
            sftp.put(localFile, remoteDir + GlobalSlash + fileName)
        elif os.path.isdir(localFile):
            dirPathLst = []
            for tempName in os.listdir(localFile):
                dirPathLst.append(localFile + GlobalSlash + tempName)
            _DoUploadFiles(sftp, dirPathLst, remoteDir + GlobalSlash + fileName)
        else:
            return False
    return True


def _CreateDirFolders(sftp, dir):
    try:
        dirs = dir.split(GlobalSlash)
        if len(dirs) > 0:
            fullDir = ""
            for eachDir in dirs:
                if not eachDir in sftp.listdir(fullDir):
                    sftp.mkdir(fullDir + eachDir)
                fullDir = fullDir + eachDir + GlobalSlash
        return True
    except Exception as e:
        UEDebug.LogException(e)
        UEDebug.LogNormal("-----------_CreateDirFolders error ! dir = " + dir)
        return False
    finally:
        pass

def SVNCommitScriptAssets(source_folder, target_folder):
    UEDebug.LogWithLine("-----SVN Commit Dlls Assets-----")
    UEDebug.LogNormal("commitPath: " + target_folder)
    commitMessage = "Commit Script Assets"

    src_files = os.listdir(source_folder)
    for file_name in src_files:
        full_file_name = os.path.join(source_folder, file_name)
        if os.path.isfile(full_file_name):
            if file_name.endswith('.txt') or file_name.endswith('.bytes'):
                shutil.copy(full_file_name, target_folder)

    if Commit(target_folder, commitMessage) == False:
        UEDebug.LogException("SVNCommit Dlls Assets Error!!!", target_folder)

def Commit(dir, message='auto commit'):
    if Cleanup(dir) == False:
        return False

    try:
        UEDebug.LogWithLine('----------SVN Commit, dir = ' + dir)
        status_command = [sys.argv[0], 'status', dir]
        changes = svn_cmd.main(status_command)

        for f in changes:
            if f.text_status == pysvn.wc_status_kind.unversioned:
                add_command = [sys.argv[0], 'add', f.path]
                svn_cmd.main(add_command)

        for f in changes:
            if f.text_status == pysvn.wc_status_kind.missing:
                del_command = [sys.argv[0], 'rm', f.path]
                svn_cmd.main(del_command)

        commit_command = [sys.argv[0], 'ci', dir, '--message', message]
        svn_cmd.main(commit_command)
        return True
    except Exception as e:
        UEDebug.LogException(e)
        UEDebug.LogWithLine('----------SVN Commit error, dir = ' + dir)
        return False
    finally:
        pass

def Cleanup(dir):
    try:
        UEDebug.LogWithLine('----------SVN Cleanup, dir = ' + dir)
        cleanup_command = [sys.argv[0], 'cleanup', dir]
        svn_cmd.main(cleanup_command)
        return True
    except Exception as e:
        UEDebug.LogException(e)
        UEDebug.LogWithLine('----------SVN Cleanup error, dir = ' + dir)
        return False
    finally:
        pass

if __name__ == "__main__":
    UEDebug.LogWithLine("-----------localFullPathFileList length = " + sys.argv[1])
    length = int(sys.argv[1])
    if length == -1:
        SVNCommitScriptAssets(sys.argv[2], sys.argv[3])
    else:
        localFullPathFileList = []
        for i in range(2, length + 2):
            localFullPathFileList.append(sys.argv[i])
        UploadFiles(localFullPathFileList, sys.argv[length + 2])
pass
