from osv import osv, fields

class depuracio_metodes(osv.osv):

	# https://doc.odoo.com/v6.0/developer/2_5_Objects_Fields_Methods/methods.html/
	def create(self, cr, uid, values, context=None):

		p_id = super(depuracio_metodes, self).create(cr, uid, values, context=context)
		p = self.browse(cr, uid, p_id, context=context)
		p_data = self.copy_data(cr, uid, p_id, default=None, context=None)
		print "Creating: "+str(self._name)
		for i in p_data:
			descripcions = self.fields_get(cr,uid,i,context=None)
			print "\t"+str(i)+": "+str(p_data[i])+" - "+str(descripcions)
		print p.id
		return p_id

	def write(self, cr, uid, ids, values, context=None):

		super(depuracio_metodes, self).write(cr, uid, ids, values, context=None)
		p = self.browse(cr, uid, ids, context=context)
		for j in p:
			p_data = self.copy_data(cr, uid, j.id, default=None, context=None)
			print "Datos"
			detalles = self.perm_read(cr,uid,ids)
			print detalles
			for i in p_data:
				descripcions = self.fields_get(cr,uid,i,context=None)
				print "\t"+str(i)+": "+str(p_data[i])+" - "+str(descripcions)

		return True

	_name = 'depuracio.metodes'
	_columns = {

	}
depuracio_metodes()

class depuracio_depproduct(osv.osv):
	_name = 'product.product'
	_inherit = ['depuracio.metodes','product.product']
	_columns = {
		'name': fields.integer('Name'),
	}
depuracio_depproduct()
