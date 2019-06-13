from odoo import fields, models, _
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    structure = fields.Many2one('res.partner',
                                string="Platform Structure",
                                domain=[('is_plateform_structure', '=', True)])

    def validate_capital_release_request(self):
        if self.release_capital_request and not self.structure:
            raise ValidationError(_('There is no structure defined on this '
                                    'capital release request.'))
        return True

    def get_sequence_register(self):
        self.validate_capital_release_request()
        return self.structure.register_sequence

    def get_sequence_operation(self):
        self.validate_capital_release_request()
        return self.structure.operation_sequence

    def get_refund_domain(self, invoice):
        refund_domain = super(AccountInvoice, self).get_refund_domain(invoice)
        refund_domain['structure'] = invoice.structure

        return refund_domain
