
 <html>
  <head>
  <style type="text/css">
	${css}  
  </style>
  </head>
  <body>
  %for o in objects :
	<div class="poster" style="page-break-inside: avoid" >
	  	<div class="logo">${helper.embed_logo_by_name('champion_logo')}</div> 
  		<div class="equips">
		<b>Match ${o.date}</b><br/>
		<b>${o.championship_id.name}</b>

		<br/><br/><br/>
		<br/><br/><br/>
		<br/><br/><br/>
		<br/><br/><br/>
		
		<table>
		<tr><td><img src="data:image/png;base64,[${o.local.shield}]" /></td><td></td> 
		<td><img src="data:image/png;base64,[${o.visitor.shield}]" /></td></tr>
		<tr><td><span class="vs">${o.local.name}</span></td><td>vs</td><td><span class="vs">${o.visitor.name}</span></td></tr><tr><td></td><td></td>
			<td>
			Precio: 45€ <br/>
		</td></tr>
  		
		</table>
		</div>
	</div>
  %endfor
  </body>
  </html>
