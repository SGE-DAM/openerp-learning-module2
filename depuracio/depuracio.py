from osv import osv, fields
import logging

class depuracio_metodes(osv.osv):

	_logger = logging.getLogger(__name__)
	# https://doc.odoo.com/v6.0/developer/2_5_Objects_Fields_Methods/methods.html/
	def depurar(self, cr, uid, ids):
		self._logger.debug("Depurar: "+str(self)+" cr "+str(cr)+" uid "+str(uid)+" ids "+str(ids))
		
		p = self.browse(cr, uid, ids, context=None)
		for j in p:
			p_data = self.copy_data(cr, uid, j.id, default=None, context=None)
			print "\tDatos"
			detalles = self.perm_read(cr,uid,ids)
			print "\t"+str(detalles)
			for i in p_data:
				descripcions = self.fields_get(cr,uid,i,context=None)
				#print "\t"+str(i)+": "+str(p_data[i])+" - "+str(descripcions)
				print "\t\t Field: "+str(i)
				if 'domain' in descripcions[str(i)]:
					print "\t\t\t Domain: "+" - "+ str(descripcions[str(i)]['domain'])
		self._logger.debug("Fin del los datos")
		self._logger.debug(self._columns)
		#methodList = [method for method in dir(self) if callable(getattr(object, method))]	
		return True

	def create(self, cr, uid, values, context=None):

		p_id = super(depuracio_metodes, self).create(cr, uid, values, context=context)
		self.depurar(cr,uid,[p_id])
		return p_id

	def write(self, cr, uid, ids, values, context=None):


		super(depuracio_metodes, self).write(cr, uid, ids, values, context=None)
		self.depurar(cr,uid,ids)

		#methodList = [method for method in dir(self) if callable(getattr(object, method))]	
		return True

	_name = 'depuracio.metodes'
	_columns = {

	}
depuracio_metodes()

class depuracio_depproduct(osv.osv):
	_name = 'product.product'
	_inherit = ['depuracio.metodes','product.product']
	_columns = {
		'namee': fields.integer('Name'),
	}
depuracio_depproduct()
