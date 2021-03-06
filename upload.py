# coding:utf-8
from file import file
import json
from qcloud_cos import *


class upload:
    """
    :type cos_client:CosClient
    """
    appid = 0
    secret_id = u""
    secret_key = u""
    region_info = u""
    cos_client = None
    bucketname = u""
    bucketPath = u""

    def initSetting(self):
        # COS设置
        try:
            file = open("/Users/Kevin/Documents/plug-in/Tecent-COS/cosup/config.json")
        except Exception as exc:
            print exc
        jsondata = json.load(file)
        self.appid = jsondata["appid"]
        self.secret_id = jsondata["secret_id"]
        self.secret_key = jsondata["secret_key"]
        self.region_info = jsondata["region_info"]
        self.bucketname = jsondata["bucketname"]
        self.bucketPath = jsondata["bucketPath"]
        self.cos_client = CosClient(self.appid, self.secret_id, self.secret_key, region=self.region_info)
        return True

    def upfile(self, f, rempath):
        """
        :param f: file
        :param rempath:
        :param remfilename:
        :return:
        """
        try:
            st_req = StatFolderRequest(self.bucketname, unicode(rempath, "utf-8"))
            st_ret = self.cos_client.stat_folder(st_req)
            if st_ret["code"] == -1:
                raise IOError("file is not found or path is not correct")
            elif st_ret["code"] == -3:
                raise IOError("time out!")
            elif st_ret["code"] == -71:
                raise IOError("operate too frequently you are in trouble")
        except IOError:
            raise
        finally:
            pass

        if st_ret["code"] == -2:
            try:
                cr_req = CreateFolderRequest(self.bucketname, unicode(rempath, "utf-8"))
                cr_ret = self.cos_client.create_folder(cr_req)
                if cr_ret["code"] == -1:
                    raise IOError("file is not found or path is not correct")
                elif cr_ret["code"] == -3:
                    raise IOError("time out!")
                elif cr_ret["code"] == -2:
                    raise IOError("404 not found")
                elif cr_ret["code"] == -71:
                    raise IOError("operate too frequently you are in trouble")
            except IOError:
                raise
            finally:
                pass
        try:
            up_req = UploadFileRequest(self.bucketname, unicode(rempath + f.filename, "utf-8"),
                                       unicode(f.abspath + "/" + f.filename, "utf-8"))
            up_ret = self.cos_client.upload_file(up_req)
            if up_ret["code"] == -1:
                raise IOError("file is not found or path is not correct")
            elif up_ret["code"] == -3:
                raise IOError("time out!")
            elif up_ret["code"] == -2:
                raise IOError("404 not found")
            elif up_ret["code"] == -71:
                raise IOError("operate too frequently you are in trouble")
        except IOError:
            raise
        finally:
            pass
        return up_ret
