from wxpy import *
import respondMsg

bot = Bot()

my_friend = bot.friends().search('机器人说话')[0]
my_friend.send('Hello, how can I help you')
# 回复 my_friend 的消息 (优先匹配后注册的函数!)
@bot.register(my_friend)
def reply_my_friend(msg):
    return_msg = respondMsg.respond(msg.text)
    return return_msg

embed()