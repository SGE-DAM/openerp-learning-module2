#!/bin/bash

read -p "Name of the module: " name

model=""
models=""

while [[ $model != "0" ]]; do
	read -p "Model name (0 for finish): " model
	if [[ $models == "" ]]; then 
		models=$model
	else
		[[ $model != "0" ]] && models="$models $model"
	fi

done

echo -e "Create module with this models: [34m$models[0m"

echo "Let's make the models"

python="from osv import osv, fields\n\n"
for model in $models
do
	echo "Model: [34m$model[0m"
	fields=""
	field=""
	
	while [[ $field != "0" ]]; do
		read -p "  Field name (0 for finish): " field
		if [[ $field != "0" ]]; then
			read -p "  Type [i]nteger [v]archar [b]oolean [F]loat [m]any2one [o]ne2many [mm]any2many [f]unction [r]elated [b]inary: " t
			read -p "  Display name: " display
			read -p "  Required True or [False]: " req;  req=${req:-False}
			case "$t" in
				i)
					field="'$field' : fields.integer('$display',required=$req)," 
					;;
				v)
					field="'$field' : fields.varchar('$display',required=$req)," 
					;;
				b)
					field="'$field' : fields.boolean('$display',required=$req)," 
					;;	
				F)
					field="'$field' : fields.float('$display',required=$req)," 
					;;
				m)
					read -p "    Many2one with witch model? $models: " other
					field="'$field' : fields.many2one('$name.$other','$display',required=$req)," 
					;;
				o)
					read -p "    one2many with witch model? $models: " other
					read -p "    one2many with witch field in $other model?: " ofield
					echo -e "    [1;33mMake sure the field $ofield exists in model $name.$other[0m"
					field="'$field' : fields.many2one('$name.$other','$ofield','$display',required=$req)," 
					;;
				mm)
					read -p "    many2many with witch model? $models: " other
					read -p "    many2many with witch field in $other model?: " ofield
					read -p "    many2many with witch field in this model?: " tfield
					echo -e "    [1;33mMake sure you use the same fields in model $name.$other[0m"
					field="'$field' : fields.many2one('$name.$other','$model_$other','$tfield','$ofield','$display',required=$req)," 
					;;
				b)
					field="'$field' : fields.binary('$display',required=$req)," 
					;;
			esac	
			if [[ $fields == "" ]]; then 
				fields="\t\t$field"
			else
				fields="$fields\n\t\t$field"
			fi
		fi
		echo ""
	done
	modelpython="class ${name}_$model(osv.osv):\n\t_name = '$name.$model'\n\t_columns = {\n$fields\n\t}\n${name}_$model()\n\n"
	echo -e "[1;37m$modelpython[0m"
	python=$python$modelpython
done

echo -e "$python"

# XML

xml="<?xml version="1.0"?>\n<openerp>\n<data>\n\n"

for model in models; do
recordf="\t<record model=\"ir.ui.view\" id=\"view_championship_team_form\">\n\t\t<field name=\"name\">championship.team.form</field>\n\t\t<field name=\"model\">res.partner</field><field name=\"arch\" type=\"xml\">\n\t\t<form string=\"championship.team\" version=\"7.0\">\n\t\t\t<sheet>\n\t\t\t\t<group>"
	for field in $(echo $python | sed -n '/${name}_$model/,/${name}_${model}()/p')
