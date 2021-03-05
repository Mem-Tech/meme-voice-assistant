class MemePost:
    def __init__(self, text, attachments):
        self.text = text
        self.atts = attachments

    def get_photo_atts(self):
        formatted_atts = []
        for elem in self.atts:
            if elem == 'type':
                if self.atts[elem] == 'photo':
                    one_att = self.atts['photo']
                    photo = 'photo{}_{}'.format(one_att['owner_id'], one_att['id'])
                    formatted_atts.append(photo)
        return formatted_atts

    def get_attachment(self):
        return 'photo{}_{}'.format(self.owner_id, self.id)

    def get_text(self):
        return self.text


class PostWithValidPhotos(MemePost):
    def __init__(self, text, attachments, photos):
        super().__init__(text, attachments)
        self.formatted_photos = photos

    def get_text(self):
        return self.text

    def get_photos(self):
        return self.formatted_photos
