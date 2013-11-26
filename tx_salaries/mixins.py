from tx_people.mixins import *


class DenormalizeOnSaveMixin(object):
    def save(self, denormalize=True, *args, **kwargs):
        obj = super(DenormalizeOnSaveMixin, self).save(*args, **kwargs)
        # TODO: Abstract into a general library
        if denormalize:
            for a in self._meta.get_all_related_objects():
                if hasattr(a.model.objects, 'denormalize'):
                    a.model.objects.denormalize(self)
        return obj
