 <html>
  <head>
  <style type="text/css">
${css}  
</style>
  </head>
  <body>
  %for o in objects :
  <div class="ticket" >

     <b>Ticket for the match ${o.date}</b><br/>
  	
  	<div>
  		${o.local.name} vs
  		${o.visitor.name}
  	</div>
  
  
  
  
  </div>
  %endfor
  </body>
  </html>
