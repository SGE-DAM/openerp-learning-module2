from osv import osv, fields
import random
from datetime import datetime
 

class championship_team(osv.osv):

	_name = 'championship.team'
	_columns = {
		'name': fields.char('Name', size=32, required=True, help='This is the name of the team'),
		'shield': fields.binary('Shield'),
		#'points': fields.function(_get_points,type='Integer',string='Points', store=False),
	}
championship_team()

class championship_teampoints(osv.osv):

	def _get_points(self, cr, uid, ids, name, arg, context=None):
		res={}        
		tots=self.browse(cr,uid,ids,context=None)
		for h in tots:
			punts = 0
			team = h.team_id.id
			champ = h.championship_id.id

			p_local = self.pool.get('championship.match').search(cr,uid,['&',('championship_id','=',champ),('local','=',team)])
			p_visitor = self.pool.get('championship.match').search(cr,uid,['&',('championship_id','=',champ),('visitor','=',team)])
			partits_local = self.pool.get('championship.match').browse(cr,uid,p_local,context=None)
			partits_visitor = self.pool.get('championship.match').browse(cr,uid,p_visitor,context=None)
			for p in partits_local:
				punts = punts + p.points_local
			for p in partits_visitor:
				punts = punts + p.points_visitor
			res[h.id] = punts

			# Necessite actualitzar tambe el camp point_v per poder ordenar self.write(cr, uid, [166, 299], {'fac_id': 21})
			print h.id
			print punts
			self.write(cr, uid, [h.id], {'point_v': punts})

			
		return res

	def _get_golsf(self, cr, uid, ids, name, arg, context=None):
		res={}        
		tots=self.browse(cr,uid,ids,context=None)
		for h in tots:
			gols = 0
			team = h.team_id.id
			champ = h.championship_id.id

			p_local = self.pool.get('championship.match').search(cr,uid,['&',('championship_id','=',champ),('local','=',team)])
			p_visitor = self.pool.get('championship.match').search(cr,uid,['&',('championship_id','=',champ),('visitor','=',team)])
			partits_local = self.pool.get('championship.match').browse(cr,uid,p_local,context=None)
			partits_visitor = self.pool.get('championship.match').browse(cr,uid,p_visitor,context=None)
			for p in partits_local:
				gols = gols + p.score_local
			for p in partits_visitor:
				gols = gols + p.score_visitor
			res[h.id] = gols
		return res

	def _get_golsc(self, cr, uid, ids, name, arg, context=None):
		res={}        
		tots=self.browse(cr,uid,ids,context=None)
		for h in tots:
			gols = 0
			team = h.team_id.id
			champ = h.championship_id.id

			p_local = self.pool.get('championship.match').search(cr,uid,['&',('championship_id','=',champ),('local','=',team)])
			p_visitor = self.pool.get('championship.match').search(cr,uid,['&',('championship_id','=',champ),('visitor','=',team)])
			partits_local = self.pool.get('championship.match').browse(cr,uid,p_local,context=None)
			partits_visitor = self.pool.get('championship.match').browse(cr,uid,p_visitor,context=None)
			for p in partits_local:
				gols = gols + p.score_visitor
			for p in partits_visitor:
				gols = gols + p.score_local
			res[h.id] = gols
		return res	

	_name = 'championship.teampoints'
	_columns = {
		'championship_id' : fields.many2one('championship.championship','Championship'),
		'team_id' : fields.many2one('championship.team','Team'),
		'points' : fields.function(_get_points,type='integer',string='Points', store=False),
		'point_v' : fields.integer('Points'),
		'score' : fields.function(_get_golsf,type='integer',string='Acumulated Score', store=False),
		'conceded' : fields.function(_get_golsc,type='integer',string='Conceded Score', store=False),
        
	}
	_order = 'point_v desc'
	
championship_teampoints()



class championship_championship(osv.osv):
	def create_calendar(self,cr, uid, ids, context=None):
		print "Calendarrrrrrrrrrrrrrrrrr"
		print ids
		c=self.browse(cr,uid,ids[0],context=None).id
		#equips= self.pool.get('championship.team').search(cr,uid,[])
		data_partit=c.start_date
		self.pool.get('championship.match').unlink(cr, uid, self.pool.get('championship.match').search(cr,uid,[('championship_id','=',c)]), context=None)
		equips=self.pool.get('championship.teampoints').browse(cr, uid, self.pool.get('championship.teampoints').search(cr,uid,[('championship_id','=',c)]), context=None)
		print equips
		equips_aux=[]
		i=0
		for e in equips:
			equips_aux.append(e.team_id.id)
			i=i+1
	#	random.shuffle(equips_aux)
		print '*******************************'
		print equips_aux
		for i in range(1, len(equips_aux)): #falta el numero de rondas calcularlo
			for j in range(0,len(equips_aux)/2):								
				self.pool.get('championship.match').create(cr, uid, {'championship_id':c,'local':equips_aux[j],'visitor':equips_aux[j+10],'round':i,'date':data_partit}, context=None)
				self.pool.get('championship.match').create(cr, uid, {'championship_id':c,'local':equips_aux[j+10],'visitor':equips_aux[j],'round':i+19,'date':data_partit}, context=None)
			aux=[]
			aux.append(equips_aux[0])
			aux.append(equips_aux[19])
			for k in range(1,19):
				aux.append(equips_aux[k])
			equips_aux=aux
			print equips_aux
			
		return True
	def populate_championship(self,cr,uid,ids,context=None):
		print "Populate"
		c=self.browse(cr,uid,ids[0],context=None).id
		equips= self.pool.get('championship.team').search(cr,uid,[])
		self.pool.get('championship.teampoints').unlink(cr, uid, self.pool.get('championship.teampoints').search(cr,uid,[('championship_id','=',c)]), context=None)
		for e in equips:
			self.pool.get('championship.teampoints').create(cr, uid, {'championship_id':c,'team_id':e}, context=None)
		return True


	_name = 'championship.championship'
	_columns = {
		'name': fields.char('Name', size=32, required=True, help='This is the name of the team'),
		#'teams': fields.many2many('championship.team','championship_teams','team_id','championship_id','Teams'),
		'teams': fields.one2many('championship.teampoints','championship_id','Teams'),
		'start_date': fields.date('Start Date'),
		'end_date': fields.date('End Date'),
		'matches': fields.one2many('championship.match','championship_id','Matches'),
	}
championship_championship()


class championship_match(osv.osv):
	def check_dates (self,cr,uid,ids,context=None):
		m = self.browse(cr, uid, ids, context=context)
		for h in m:
			if (h.date < h.championship_id.start_date) or (h.date > h.championship_id.end_date):
				return False
		return True
  	
	_name = 'championship.match'
	_columns = {
		'date': fields.date('Date'),
		'championship_id': fields.many2one('championship.championship','Championship'),
		'round': fields.integer('Round'),
		'local': fields.many2one('championship.team','Local Team'),
		'visitor': fields.many2one('championship.team','Visitor Team'),
		'score_local': fields.integer('Score Local'),
		'score_visitor': fields.integer('Score Visitor'),
		'points_local': fields.integer('Points Local'),
		'points_visitor': fields.integer('Points Visitor'),

	}
	_constraints = [
		(check_dates,"The date of the match isn't between the dates of the championship", ["date"]),
	]

championship_match()
