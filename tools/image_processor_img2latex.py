from PIL import Image
from .image_processing_nougat import NougatImageProcessor

class NougatLaTexProcessor(NougatImageProcessor):

    def __init__(self, img_height=224, img_width=560, **kwargs):
        self.imgH = img_height
        self.imgW = img_width
        self.maxH = img_height // 2
        super(NougatLaTexProcessor, self).__init__(**kwargs)

    def __call__(self, images, **kwargs):
        images = self._rescale(images)
        images[0].save("show.jpg")
        print(images[0].size)
        return self.preprocess(images, **kwargs)

    # def _rescale(self, images_list):
    #     process_images = []
    #     for images in images_list:
    #         Image.new("RGB", (images.width+10,images.height+10))
    #         if images.height < self.maxH:
    #             empty_img = Image.new("RGB", (self.imgW, self.imgH))
    #             target_w = max(1, int(images.width / images.height * self.maxH))
    #             if target_w > self.imgW:
    #                 target_w = self.imgW
    #                 target_h = max(1, int(self.imgW / images.width * images.height))
    #             else:
    #                 target_h = self.maxH
    #             images = images.resize((target_w, target_h))
    #             start_h = (self.imgH - target_h) // 2
    #             start_w = 0
    #             empty_img.paste(images, (start_w, start_h))
    #             images = empty_img
    #         images.save("show.jpg")
    #         process_images.append(images)
    #     return process_images

    def _rescale(self, images_list):
        process_images = []
        for image in images_list:
            if image.height < self.maxH:
                empty_img = Image.new("RGB", (self.imgW, self.imgH), "white")
                max_scale_width = 560 / image.width
                max_scale_height = 112 / image.height # 比较特殊
                max_scale = min(max_scale_width, max_scale_height)
                scale = max_scale
                scaled_width, scaled_height = int(image.width * scale), int(image.height * scale)
                scaled_image = image.resize((scaled_width, scaled_height))
                start_h = (224 - scaled_height) // 2
                # start_h = 224 - scaled_height
                start_w = 0
                empty_img.paste(scaled_image, (start_w, start_h))
                image = empty_img
            # image.save("show.jpg")
            process_images.append(image)
        return process_images
        

# /home/lixumin/project/xizhi_OCR/xizhi-latex-beta/show.jpg

