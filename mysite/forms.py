class FormBase(object):
    def __init__(self, *args, **kwargs):
        super(FormBase, self).__init__()

    def get_all_fields(self):
        fields = {}
        for k, v in self.fields.iteritems():
            if hasattr(self, 'instance'):
                fields[k] = getattr(self.instance, k)
            elif hasattr(self, 'cleaned_data'):
                fields[k] = getattr(self.cleaned_data, k)
            else:
                raise Exception("Field does not exist")
        return fields

    @property
    def list(self):
        pass

    @property
    def show(self):
        pass
