from osv import osv, fields
import random
from datetime import datetime
from datetime import timedelta
 

class championship_team(osv.osv):
	_inherit = 'res.partner'
	#_name = 'championship.team'
	_columns = {
		'isteam' : fields.boolean('Is Team'),
		'players' : fields.one2many('res.partner','team_id','Players'),
		#'name': fields.char('Name', size=32, required=True, help='This is the name of the team'),
		#'shield': fields.binary('Shield'),
		#'points': fields.function(_get_points,type='Integer',string='Points', store=False),
	}
championship_team()

class championship_player(osv.osv):
	def get_matches(self, cr, uid, ids, name, arg, context=None):
		res={}      
		tots=self.browse(cr,uid,ids,context=None)
		for h in tots:
			matches=[]
			m=self.pool.get('sale.order.line').search(cr,uid,[])
			m=self.pool.get('sale.order.line').browse(cr,uid,m,context=None)
			for match in m:
				if h in match.players_local:
					matches.append(match.id)	
				if h in match.players_visitor:
					matches.append(match.id)	
			res[h.id]=matches
		return res

	_inherit = 'res.partner'
	#_name = 'championship.player'
	_columns = {
		'isplayer' : fields.boolean('Is player'),
		'born_date': fields.date('Born Date'),
		'country': fields.many2one('res.country','Country'),
		'position': fields.selection((('p','Goalkeeper'), ('d','Defender'),('c','MidField'),('f','Front')),'Position'),
		'team_id' : fields.many2one('res.partner','Team',domain="[('isteam','=', True)]"),
		'matches' : fields.function(get_matches,type='many2many',relation='sale.order.line',string="Matches",store=False),
	}
championship_player()


class championship_teampoints(osv.osv):

	def get_points(self, cr, uid, ids, name, arg, context=None):
		res={}      
		tots=self.browse(cr,uid,ids,context=None)
			
		for h in tots:
			punts = 0
			golsf = 0
			golsc = 0
			team = h.partner_id.id
			champ = h.championship_id.id

			if arg:
		#		print str(arg)+str(arg.round)
		#		print tots
				p_local = self.pool.get('sale.order.line').search(cr,uid,['&',('championship_id','=',champ),('local','=',team),('round','<=',arg.round)])
				p_visitor = self.pool.get('sale.order.line').search(cr,uid,['&',('championship_id','=',champ),('visitor','=',team),('round','<=',arg.round)])
		#		print str(p_local)+str(p_visitor)
			else:
				p_local = self.pool.get('sale.order.line').search(cr,uid,['&',('championship_id','=',champ),('local','=',team)])
				p_visitor = self.pool.get('sale.order.line').search(cr,uid,['&',('championship_id','=',champ),('visitor','=',team)])
			partits_local = self.pool.get('sale.order.line').browse(cr,uid,p_local,context=None)
			partits_visitor = self.pool.get('sale.order.line').browse(cr,uid,p_visitor,context=None)
			for p in partits_local:
				punts = punts + p.points_local
				golsf = golsf + p.score_local
				golsc = golsc + p.score_visitor
			for p in partits_visitor:
				punts = punts + p.points_visitor
				golsc = golsc + p.score_local
				golsf = golsf + p.score_visitor
			res[h.id] = punts
			#print punts
			# Necessite actualitzar tambe el camp point_v per poder ordenar self.write(cr, uid, [166, 299], {'fac_id': 21})
		#	print h.id
		#	print punts
			if not arg: 
				self.write(cr, uid, [h.id], {'point_v': punts,'score' : golsf,'conceded': golsc})

			
		return res


	_inherit = 'sale.order'
	#_name = 'championship.teampoints'
	_columns = {
		'isteam' : fields.boolean('Team enrole'),
		'championship_id' : fields.many2one('championship.championship','Championship'),
	#	'team_id' : fields.many2one('res.partner','Team'),
		'points' : fields.function(get_points,type='integer', string='Points', store=False),
		'point_v' : fields.integer('Points',readonly=True),
		'score' : fields.integer('Score', readonly=True),
		'conceded' : fields.integer('Conceded', readonly=True),
		'rounds': fields.one2many('championship.round','teampoint','Rounds'),                 
	}
	_order = 'point_v desc'
	
championship_teampoints()



class championship_championship(osv.osv):
	def create_calendar(self,cr, uid, ids, context=None):
		print "******Generar calendari ***********************************"
		print ids
		c=self.browse(cr,uid,ids[0],context=None).id #obtindre el campionat
		#equips= self.pool.get('championship.team').search(cr,uid,[])
		data_partit=self.browse(cr,uid,ids[0],context=None).start_date
		s_o_l=self.pool.get('sale.order.line')
		rondas=self.pool.get('championship.round')
		s_o=self.pool.get('sale.order')
		s_o_l.unlink(cr, uid, s_o_l.search(cr,uid,[('championship_id','=',c)]), context=None)
		rondas.unlink(cr,uid,rondas.search(cr,uid,[('teampoint.championship_id','=',c)]),context=None)
		equips=s_o.browse(cr, uid, s_o.search(cr,uid,[('championship_id','=',c)]), context=None)
		print equips
		equips_aux=[]
		i=0
		for e in equips:
			equips_aux.append(e.partner_id.id)
			i=i+1
		random.shuffle(equips_aux)
		print '*******************************'
		print equips_aux
		for i in range(1, len(equips_aux)): #falta el numero de rondas calcularlo
			for j in range(0,len(equips_aux)/2):
				date_p = datetime.strptime(data_partit, "%Y-%m-%d")
				date_p = date_p + timedelta(days=7*i)
				date_p2 = date_p + timedelta(days=7*20)
				order1= s_o.browse(cr, uid, s_o.search(cr,uid,['&',('championship_id','=',c),('partner_id','=',equips_aux[j])]), context=None)
				order1=order1[0] 
				order2= s_o.browse(cr, uid, s_o.search(cr,uid,['&',('championship_id','=',c),('partner_id','=',equips_aux[19-j])]), context=None)
				order2=order2[0]
				print order1.partner_id.name+"vs"+order2.partner_id.name 
				s_o_l.create(cr, uid, {
							'name': order1.partner_id.name+"vs"+order2.partner_id.name,
							'order_id': order1.id,  
							'championship_id':c,
							'local':equips_aux[j],
							'visitor':equips_aux[19-j],
							'round':i,
							'points_local': random.randint(0,3),
							'points_visitor': random.randint(0,3),
							'price_unit': 1000,
							'date':date_p}, context=None)
				s_o_l.create(cr, uid, {
							'name': order2.partner_id.name+"vs"+order1.partner_id.name,
							'order_id': order2.id,  
							'championship_id':c,
							'local':equips_aux[19-j],
							'visitor':equips_aux[j],
							'points_local': random.randint(0,3),
							'points_visitor': random.randint(0,3),
							'price_unit': 1000,
							'round':i+19,
							'date':date_p2}, context=None)
				rondas.create(cr, uid, {'round': i,'teampoint':order1.id},context=None)
				rondas.create(cr, uid, {'round': i+19,'teampoint':order2.id},context=None)
				rondas.create(cr, uid, {'round': i,'teampoint':order2.id},context=None)
				rondas.create(cr, uid, {'round': i+19,'teampoint':order1.id},context=None)
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
		equips= self.pool.get('res.partner').search(cr,uid,[('isteam','=','True')])
		self.pool.get('sale.order').unlink(cr, uid, self.pool.get('sale.order').search(cr,uid,[('championship_id','=',c)]), context=None)
		for e in equips:
			self.pool.get('sale.order').create(cr, uid, {'championship_id':c,
									'partner_id':e,
									'partner_invoice_id':e,
									'partner_shipping_id':e,
									'pricelist_id':1,
									'isteam':True}, context=None)
		return True

	def print_championship(self,cr,uid,ids,context=None):
		print "Championship"
		c=self.browse(cr,uid,ids[0],context=None).id
		equips=self.pool.get('sale.order').search(cr,uid,[('championship_id','=',c)])
		teams=self.pool.get('sale.order').browse(cr,uid,equips,context=None)
		for t in teams:
			print t.partner_id.name
			partits=self.pool.get('sale.order.line').search(cr,uid,[('order_id','=',t.id)])
			partits=self.pool.get('sale.order.line').browse(cr,uid,partits,context=None)
			for p in partits:	
				print "  "+p.name+" "+str(p.date)
		return True

	_name = 'championship.championship'
	_columns = {
		'name': fields.char('Name', size=32, required=True, help='This is the name of the team'),
		#'teams': fields.many2many('championship.team','championship_teams','team_id','championship_id','Teams'),
		'teams': fields.one2many('sale.order','championship_id','Teams'),
		'start_date': fields.date('Start Date'),
		'end_date': fields.date('End Date'),
		'matches': fields.one2many('sale.order.line','championship_id','Matches'),
	}

championship_championship()


class championship_match(osv.osv):
	def check_dates (self,cr,uid,ids,context=None):
		m = self.browse(cr, uid, ids, context=context)
		for h in m:
			if (h.date < h.championship_id.start_date) or (h.date > h.championship_id.end_date):
				return False
		return True
	def check_dates2 (self,cr,uid,ids,context=None):
		m = self.browse(cr, uid, ids, context=context)
		for h in m:
			same_date=self.search(cr,uid,['&',('date','=',h.date),('id','!=',h.id)])
			same_date=self.browse(cr,uid,same_date, context=context)
			#print same_date
			#print h
			for s in same_date:
				if (s.local == h.local) or (s.local == h.visitor) or (s.visitor == h.local) or (s.visitor == h.visitor):
					return False
						
		return True
  	
	_inherit = 'sale.order.line'
	#_name = 'championship.match'
	_columns = {
		'date': fields.date('Date'),
		'championship_id': fields.many2one('championship.championship','Championship'),
		'round': fields.integer('Round'),
		'local': fields.many2one('res.partner','Local Team'),
		'visitor': fields.many2one('res.partner','Visitor Team'),
		'score_local': fields.integer('Score Local'),
		'score_visitor': fields.integer('Score Visitor'),
		'points_local': fields.integer('Points Local'),
		'points_visitor': fields.integer('Points Visitor'),
		'players_local' : fields.many2many('res.partner','alignment_local','match_id','player_id','Players Local'),
		'players_visitor' : fields.many2many('res.partner','alignment_visitor','match_id','player_id','Players Visitor'),


	}
	_constraints = [
		(check_dates,"The date of the match isn't between the dates of the championship", ["date"]),
		(check_dates2,"One team of this match has other match the same day", ["date"]),
	]

	_order = 'round'
championship_match()

class championship_round(osv.osv):
	
	def _get_points(self, cr, uid, ids, name, arg, context=None):
		res={}
		for h in self.browse(cr,uid,ids,context=None):
			a=h.teampoint.get_points(h.teampoint,h)
			#print "puntos"
			res[h.id]=a[h.teampoint.id]
			self.write(cr,uid,[h.id],{'point_v':res[h.id]})
		return res			

	_name = 'championship.round'
	_columns = {
		'round' :fields.integer('Round'),
		'teampoint' : fields.many2one('sale.order','Teampoints'),
		'team' : fields.related('teampoint','partner_id',type='many2one',relation='res.partner',string='Team',store=False),
		'championship' : fields.related('teampoint','championship_id',type='many2one',relation='championship.championship',string='Championship',store=False),
		'points' : fields.function(_get_points,type='integer', string='Points', store=False),
		'point_v' : fields.integer('Points'),
	}
