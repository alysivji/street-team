class Event:
    def match(self, event):
        return event["type"] == self.type

    def perform(self, event):
        pass


class UploadImage(Event):
    type = "upload_image"


class CropImage(Event):
    type = "crop_image"


class AddCaption(Event):
    type = "add_caption"


class ModifyCaption(Event):
    type = "modify_caption"


class SubmitForReview(Event):
    type = "submit_for_review"


class RejectPost(Event):
    type = "reject_post"


class ApprovePost(Event):
    type = "approve_post"
