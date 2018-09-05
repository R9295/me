class StyledForm:
    def __init__(self, *args, **kwargs):
        super(StyledForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            v.widget.attrs['class'] = self.field_css.get(k)
            if self.field_icons:
                v.widget.icon = self.field_icons.get(k)
