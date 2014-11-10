from osv import osv, fields
import random
from datetime import datetime
from datetime import timedelta
import openerp.tools as tools

class parking_car(osv.osv):

	_name = 'parking.car'
	_columns = {
		'name': fields.char('ID', size=10, required=True),
		'tickets': fields.one2many('parking.ticket','car','Tickets'),
	}
parking_car()

class parking_place(osv.osv):
	def _get_total(self, cr, uid, ids, name, arg, context=None):
                res = {}
                p = self.browse(cr, uid, ids, context=context)
                for h in p:
			total=0
			for t in h.tickets:
				total=total+t.price
			res[h.id]=total	
                return res

	_name = 'parking.place'
	_columns = {
		'level' : fields.integer('Level', required=True),
		'num' : fields.integer('Number', required=True),
		'tickets': fields.one2many('parking.ticket','place','Tickets'),
		'total' :fields.function(_get_total,type='float',string='Total',store=False),
	}
		
parking_place()

class parking_ticket(osv.osv):
	
	def _get_price (self, cr, uid, ids, name, arg, context=None):
		res = {}
		t = self.browse(cr, uid, ids, context=context)
		for h in t:
			print h.date_in
			print tools.DEFAULT_SERVER_DATETIME_FORMAT
			a=datetime.strptime(h.date_in,"%Y-%m-%d %H:%M:%S")
			b=datetime.strptime(h.date_out,"%Y-%m-%d %H:%M:%S")	
			timedelta = b - a
			print timedelta.seconds
			res[h.id]=(timedelta.seconds/60)*0.2		
		return res
	
	_name = 'parking.ticket'
	_columns = {
		'car': fields.many2one('parking.car','Car ID', required=True),
		'place': fields.many2one('parking.place','Place',required=True),
		'date_in': fields.datetime('Date In',required=True),
		'date_out': fields.datetime('Date Out',required=False),
		'price': fields.function(_get_price,type='float',string='Price',store=False),
		'payment': fields.selection((('c','Credit Card'), ('m','Money'),('p','Partner')),'Payment Mode'),
	}
parking_ticket()
