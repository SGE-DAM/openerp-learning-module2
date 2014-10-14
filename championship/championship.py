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
		'score' : fields.function(_get_golsf,type='integer',string='Acumulated Score', store=False),
		'conceded' : fields.function(_get_golsc,type='integer',string='Conceded Score', store=False),
        
	}
championship_teampoints()



class championship_championship(osv.osv):
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
championship_match()
