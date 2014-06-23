from PIL import Image
from django.views.generic.edit import FormView
from django.views.generic import DetailView
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from .forms import UploadURLForm
from .utils import *
from .models import UploadedImage


class UploadURLView(FormView):
    form_class = UploadURLForm
    template_name = "image_uploader/upload.html"

    def get_success_url(self):
        return reverse("upload-detail", args=[self.uploaded_image.pk, ])

    def form_valid(self, form):
        def _invalidate(msg):
            form.errors['url'] = [msg, ]
            return super(UploadURLView, self).form_invalid(form)

        url = form.data['url']
        domain, path = split_url(url)
        filename = get_url_tail(path)

        if not image_exists(domain, path):
            return _invalidate(_("Couldn't retreive image. (There was an error reaching the server)"))

        fobject = retrieve_image(url)
        if not valid_image_mimetype(fobject):
            return _invalidate(_("Downloaded file was not a valid image"))

        pil_image = Image.open(fobject)
        if not valid_image_size(pil_image)[0]:
            return _invalidate(_("Image is too large (> 4mb)"))

        django_file = pil_to_django(pil_image)
        self.uploaded_image = UploadedImage()
        self.uploaded_image.image.save(filename, django_file)
        self.uploaded_image.save()

        return super(UploadURLView, self).form_valid(form)

class UploadDetailView(DetailView):
    model = UploadedImage
    context_object_name = "image"
    template_name = "image_uploader/detail.html"