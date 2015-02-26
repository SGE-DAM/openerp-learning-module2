from osv import osv, fields

class depuracio_deppartner(osv.osv):
	#_name = 'depuracio.deppartner'
	# https://doc.odoo.com/v6.0/developer/2_5_Objects_Fields_Methods/methods.html/
	def create(self, cr, uid, values, context=None):

		p_id = super(depuracio_deppartner, self).create(cr, uid, values, context=context)
		p = self.browse(cr, uid, p_id, context=context)
		p_data = self.copy_data(cr, uid, p_id, default=None, context=None)
		print "Datos del res.partner: "
		for i in p_data:
			descripcions = self.fields_get(cr,uid,i,context=None)
			print "\t"+str(i)+": "+str(p_data[i])+" - "+str(descripcions)

		return p_id

	def write(self, cr, uid, ids, values, context=None):

		super(depuracio_deppartner, self).write(cr, uid, ids, values, context=None)
		p = self.browse(cr, uid, ids, context=context)
		for j in p:
			p_data = self.copy_data(cr, uid, j.id, default=None, context=None)
			print "Datos del res.partner: "
			for i in p_data:
				descripcions = self.fields_get(cr,uid,i,context=None)
				print "\t"+str(i)+": "+str(p_data[i])+" - "+str(descripcions)

		return True

	_inherit = 'res.partner'
	_columns = {

	}
depuracio_deppartner()

"""class depuracio_depproduct(osv.osv):
	#_name = 'depuracio.depproduct'
	_inherit = 'product.product'
	_columns = {

	}
depuracio_depproduct()
"""
