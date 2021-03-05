def write_msg_vk(api, vk, user_id, message):
    random_id = api.utils.get_random_id()
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random_id})
    #vk_api.upload.VkUpload()
