import os
import itchat
import time
from bs4 import BeautifulSoup

class ParseData:
    # 文件临时存储页
    rec_tmp_dir = os.path.join(os.getcwd(), 'tmp/')
    # 存储数据的字典
    rec_msg_dict = {}

    @staticmethod
    def note_parse_data(msg):
        if msg['MsgType'] == 49:
            print('红包转账')
            msg_content = '红包转账'
        # 红包消息
        elif msg['MsgType'] == 10000:
            msg_content = msg['Text']
        # 消息撤回
        elif msg['MsgType'] == 10002:
            msg_content = msg['Text']+ParseData.get_oldmsg(msg['Content'])
        else:
            print('其他类型')
            msg_content = '其他类型'+str(msg['MsgType'])
        return msg_content


    # 查找撤回的消息
    @staticmethod
    def get_oldmsg(data):
        bs = BeautifulSoup(data, 'html.parser')
        oldmsgid = bs.msgid.string
        value = ParseData.rec_msg_dict.get(oldmsgid)
        if value == None:
            msg = ',撤回的内容未找到'
        else:
            msg_content = value['msg_content']
            msg = ',撤回的内容为:'+msg_content
        return msg


    # 通过UserName获取用户名
    @staticmethod
    def get_friend_remarkname(userName):
        friend_data = itchat.search_friends(userName=userName)

        if userName.find('@') == -1:
            return userName

        if friend_data['RemarkName']:
            return friend_data['RemarkName']
        else:
            return friend_data['NickName']

    @staticmethod
    def get_chatroom_nickname(userName):
        chatroom_data = itchat.search_chatrooms(userName=userName)
        return chatroom_data['NickName']

    # 时间戳转换
    @staticmethod
    def get_time(ts):
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
        return dt

    # 获取名片中的微信号，昵称与性别信息
    @staticmethod
    def get_card_nickname(data):
        bs = BeautifulSoup(data, 'html.parser')
        username = bs.msg['username']
        nickname = bs.msg['nickname']
        sex = ParseData.get_sex(bs.msg['sex'])

        msg = '推荐好友名片(微信号:'+username+',昵称:'+nickname+',性别:'+sex+')'
        return msg

    # 获取好友请求中的微信号，昵称与性别信息
    @staticmethod
    def get_friend_info(data):
        bs = BeautifulSoup(data, 'html.parser')
        alias = bs.msg['alias']
        fromnickname = bs.msg['fromnickname']
        sex = ParseData.get_sex(bs.msg['sex'])
        msg = '好友请求(微信号:'+alias+',昵称:'+fromnickname+',性别:'+sex+')'
        return msg

    @staticmethod
    def get_sex(data):
        if data == '0':
            sex = '未知'
        elif data == '1':
            sex = '男'
        elif data == '2':
            sex = '女'
        else:
            sex = data
        return sex