 <html>
  <head>
  <style type="text/css">
${css}  
</style>
  </head>
  <body>
  %for o in objects :
  
  <div class="address">
     <b>${o.date |entity}</b><br/>
  	
  	<div class="header">
  		<span class="header" style="width: 20%;">${o.local}</span>
  		<span class="header" style="width: 10%;">${o.visitor}</span>
  	</div>
  
  
  
  
  </div>
  %endfor
  </body>
  </html>
