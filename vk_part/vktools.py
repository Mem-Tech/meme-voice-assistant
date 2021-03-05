from Classes.MemePost import MemePost, PostWithValidPhotos
from settings import VK_TOKEN, VK_USER_ID, VK_PUBLIC_IDS
import vk_api
import secrets


def write_msg_vk_user(api, vk, user_id, message, attachment):
    random_id = api.utils.get_random_id()
    vk.method("messages.send",
              {"user_id": user_id, "message": message, "attachment": attachment, "random_id": random_id})


def write_msg_vk_chat(api, vk, chat_id, message, attachment):
    random_id = api.utils.get_random_id()
    vk.messages.send(chat_id=chat_id, message=message,attachment=attachment, random_id=random_id)
    # vk.method("messages.send",
    #           {"chat_id": chat_id, "message": message, "attachment": attachment, "random_id": random_id})


def get_memes(vk_api, vk_session, id, number_of_posts):
    #tools = vk_api.VkTools(vk_session)

    vk = vk_session.get_api()
    wall = vk.wall.get(owner_id=id, count=number_of_posts)

    meme_posts = []

    for post in wall['items']:
        print(post['text'])
        text = post['text']
        if post['marked_as_ads'] == 0:
            for att in post['attachments']:
                meme_post = MemePost(text, att)
                meme_posts.append(meme_post)

    return meme_posts


# vk_session = vk_api.VkApi(VK_USER_LOGIN, VK_USER_PASS)
vk_session = vk_api.VkApi(token=VK_TOKEN)


def get_random_meme(ids):
    rand_id = secrets.choice(ids)
    posts = get_memes(vk_api, vk_session, rand_id, 50)
    ext_posts = []
    for pst in posts:
        x = PostWithValidPhotos(pst.text, pst.atts, pst.get_photo_atts())
        ext_posts.append(x)

    #ext_posts = [x for x in ext_posts if x]
    not_null_atts_post = []
    print(ext_posts)
    for post in ext_posts:
        if post.formatted_photos:
            not_null_atts_post.append(post)

    rand_meme = secrets.choice(not_null_atts_post)

    return rand_meme


#post = get_random_meme(VK_PUBLIC_IDS)
