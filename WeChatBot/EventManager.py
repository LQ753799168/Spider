import itchat
from itchat.content import *
from WeChatBot.ParseData import *

class EventManager:
    def __init__(self):
        print('路径：', ParseData.rec_tmp_dir)
        if not os.path.exists(ParseData.rec_tmp_dir):
            os.mkdir(ParseData.rec_tmp_dir)

    @staticmethod
    # 好友信息监听（附件，名片，好友请求，红包，转账，定位，通知（消息撤回等），图片，分享，文字，短视频，语音）
    @itchat.msg_register([ATTACHMENT, CARD, FRIENDS,MAP,
                          NOTE, PICTURE, RECORDING, SHARING,
                          TEXT, VIDEO, VOICE], isFriendChat=True)
    def information(msg):
        # print("好友信息: ", msg)
        msg_id = msg['MsgId']
        msg_create_time = ParseData.get_time(msg['CreateTime'])
        msg_type = msg['Type']
        msg_from_user = ParseData.get_friend_remarkname(msg['FromUserName'])
        msg_to_user = ParseData.get_friend_remarkname(msg['ToUserName'])
        if msg_type == 'Text':
            msg_content = msg['Text'].replace('\n', ' ')
        elif msg_type == 'Picture' or msg_type == 'Recording' \
                or msg_type == 'Video' or msg_type == 'Attachment':
            msg_content = msg['FileName']
            msg.download(msg.fileName)
            msg['Text'](ParseData.rec_tmp_dir + msg['FileName'])
        elif msg_type == 'Card':
            msg_content = ParseData.get_card_nickname(msg['Content'])
        elif msg_type == 'Map':
            msg_content = '发送位置信息:'+msg['Content']
        elif msg_type == 'Note':
            msg_content = ParseData.note_parse_data(msg)
        elif msg_type == 'Friends':
            msg_content = ParseData.get_friend_info(msg['Content'])
        elif msg_type == 'Sharing':
            msg_content = '标题:' + msg['Text']
        else:

            msg_content = ''
        ParseData.rec_msg_dict.update({
            msg_id: {
                'msg_create_time': msg_create_time,
                'msg_type': msg_type,
                'msg_from_user': msg_from_user,
                'msg_to_user': msg_to_user,
                'msg_content': msg_content
            }
        })
        print('好友信息:', '发送时间:', msg_create_time, '类型:', msg_type, '发送者:', msg_from_user,
              '接收者:', msg_to_user, '内容:', msg_content)

    # 群聊信息监听
    @staticmethod
    @itchat.msg_register([TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
    def information(msg):
        # print("群聊信息: ", msg)
        msg_create_time = ParseData.get_time(msg['CreateTime'])
        msg_type = msg['Type']
        msg_chatroom_name = msg['User']['NickName']
        msg_user = msg['ActualNickName']
        if msg_type == 'Text':
            if msg.isAt:
                print("有人at我")
            msg_content = msg['Text'].replace('\n', ' ')
        elif msg_type == 'Picture' or msg_type == 'Recording' \
                or msg_type == 'Video' or msg_type == 'Attachment':
            msg_content = r"" + msg['FileName']
        else:
            msg_content = ''
        print('群聊信息:', '发送时间:', msg_create_time, '类型:', msg_type, '群名:', msg_chatroom_name, '发送者:', msg_user, '内容:',
              msg_content)

    # 公众号信息监听
    @staticmethod
    @itchat.msg_register([TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO], isMpChat=True)
    def information(msg):
        print('公众号信息:', msg)

    # # 系统信息监听
    # @staticmethod
    # @itchat.msg_register(SYSTEM, isFriendChat=True)
    # def information(msg):
    #     print('系统信息isFriendChat:', msg)
    #
    # # 系统信息监听
    # @staticmethod
    # @itchat.msg_register(SYSTEM, isGroupChat=True)
    # def information(msg):
    #     print('系统信息isGroupChat:', msg)
    #
    # # 系统信息监听
    # @staticmethod
    # @itchat.msg_register(SYSTEM, isMpChat=True)
    # def information(msg):
    #     print('系统信息isMpChat:', msg)