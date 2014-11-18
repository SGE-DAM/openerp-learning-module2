from osv import osv, fields

class asteroids_sonda(osv.osv):
	def _get_x(self,cr, uid, ids, name, arg, context=None):
		res={}
		t=self.browse(cr,uid,ids,context=None)
		for h in t:
			x=h.xi
			for d in h.despls:
				x=x+d.x	
			res[h.id]=x
		return res

	def _get_y(self,cr, uid, ids, name, arg,  context=None):
		res={}
		t=self.browse(cr,uid,ids,context=None)
		for h in t:
			y=h.yi
			for d in h.despls:
				y=y+d.y	
			res[h.id]=y
		return res

	def _get_z(self,cr, uid, ids, name, arg, context=None):
		res={}
		t=self.browse(cr,uid,ids,context=None)
		for h in t:
			z=h.zi
			for d in h.despls:
				z=z+d.z	
			res[h.id]=z
		return res

	_name = 'asteroids.sonda'
	_columns = {
		'name' : fields.char('Name',required=True),
		'x' : fields.function(_get_x,type='integer',string='X', store=False),
		'y' : fields.function(_get_y,type='integer',string='Y', store=False),
		'z' : fields.function(_get_z,type='integer',string='Z', store=False),
		'xi' : fields.integer('X init',required=False),
		'yi' : fields.integer('Y init',required=False),
		'zi' : fields.integer('Z init',required=False),
		'despls': fields.one2many('asteroids.despl','sonda_id','Desp'),
	}
asteroids_sonda()

class asteroids_despl(osv.osv):
	_name = 'asteroids.despl'
	_columns = {
		'date' : fields.date('Date',required=False),
		'sonda_id' : fields.many2one('asteroids.sonda','Sonda',required=False),
		'x' : fields.integer('X',required=False),
		'y' : fields.integer('Y',required=False),
		'z' : fields.integer('Z',required=False),
	}
asteroids_despl()


