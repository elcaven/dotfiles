from qtile_extras.widget import TextBox
from qtile_extras.widget.mixins import TooltipMixin

class TooltipTextBox(TextBox, TooltipMixin):

    def __init__(self, *args, **kwargs):
        TextBox.__init__(self, *args, **kwargs)
        TooltipMixin.__init__(self, **kwargs)
        self.add_defaults(TooltipMixin.defaults)

        # The tooltip text is set in the following variable
        self.tooltip_text = "Tooltip message goes here..."
