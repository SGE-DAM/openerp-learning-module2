from osv import osv, fields

class asteroids_sonda(osv.osv):
	_name = 'asteroids.sonda'
	_columns = {
		'name' : fields.char('Name',required=False),
		'x' : fields.integer('X',required=False),
		'y' : fields.integer('Y',required=False),
		'z' : fields.integer('Z',required=False),
		'xi' : fields.integer('X inicial',required=False),
		'yi' : fields.integer('Y inicial',required=False),
		'zi' : fields.integer('Z inicial',required=False),
	}
asteroids_sonda()

class asteroids_despl(osv.osv):
	_name = 'asteroids.despl'
	_columns = {
		'date' : fields.date('Date',required=False),
		'asteroid_id' : fields.many2one('asteroids.sonda','Asteroid',required=False),
		'x' : fields.integer('X',required=False),
		'y' : fields.integer('Y',required=False),
		'z' : fields.integer('Z',required=False),
	}
asteroids_despl()


