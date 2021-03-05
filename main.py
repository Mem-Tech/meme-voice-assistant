import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from hotword import listenmic
# API токен сообщества (юзера)
mytoken = 'ваш токен'

# Voice assistant
listenmic()

# Speech synthesizer


# Wall post parser


# Send meme
def write_msg(user_id, message):
    random_id = vk_api.utils.get_random_id()
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random_id})


# Auth
vk = vk_api.VkApi(token=mytoken)
longpoll = VkLongPoll(vk)



#if __name__ == '__main__':
#    print_hi('PyCharm')

