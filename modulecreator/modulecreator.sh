#!/bin/bash

read -p "Name of the module: " name

model=""
models=""

echo -e "\nCreate the models:\n"
while [[ $model != "0" ]]; do
	read -p "Model name (0 for finish): " model
	if [[ $models == "" ]]; then 
		models=$model
	else
		[[ $model != "0" ]] && models="$models $model"
	fi

done

echo -e "\nCreating module with this models: [34m$models[0m"

echo "Let's make the models"

python="from osv import osv, fields\n\n"
xml="<?xml version=\"1.0\"?>\n<openerp>\n<data>\n\n"
xml="$xml<menuitem name=\"$name\" id=\"menu_$name\"/>\n<menuitem name=\"Management\" id=\"menu_${name}_management\"  parent=\"menu_$name\"/>\n\n"

for model in $models
do
	echo "Model: [34m$model[0m"
	fields=""
	field=""
	
	recordform="\t<record model=\"ir.ui.view\" id=\"view_${name}_${model}_form\">\n\t\t<field name=\"name\">$name.$model.form</field>\n\t\t<field name=\"model\">$name.$model</field><field name=\"arch\" type=\"xml\">\n\t\t<form string=\"$name.$model\" version=\"7.0\">\n\t\t\t<sheet>\n\t\t\t\t<group>\n"
	recordtree="\t<record model=\"ir.ui.view\" id=\"view_${name}_${model}_tree\">\n\t\t<field name=\"name\">$name.$model.tree</field>\n\t\t<field name=\"model\">$name.$model</field><field name=\"arch\" type=\"xml\">\n\t\t<tree string=\"$name.$model\">\n"
	fieldsxml=""

	functions=""
	
	while [[ $field != "0" ]]; do
		read -p "  Field name (0 for finish): " field
		if [[ $field != "0" ]]; then
			fieldsxml="$fieldsxml\t\t\t<field name=\"$field\"/>\n" 
			read -p " Type [i]nteger [c]har [b]oolean [F]loat [m]any2one [o]ne2many [mm]any2many [f]unction [b]inary [d]ate: " t
			read -p "  Display name: " display
			read -p "  Required True or [False]: " req;  req=${req:-False}
			case "$t" in
				i)
					field="'$field' : fields.integer('$display',required=$req),"

					;;
				c)
					field="'$field' : fields.char('$display',required=$req)," 
					;;
				b)
					field="'$field' : fields.boolean('$display',required=$req)," 
					;;	
				F)
					field="'$field' : fields.float('$display',required=$req)," 
					;;
				m)
					read -p "    Many2one with witch model?[34m $models[0m: " other
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
				d)
					field="'$field' : fields.date('$display',required=$req)," 
					;;
				f)
					functions="$functions\n\tdef _get_$field(self,cr, uid, ids, name, arg, context=None):\n\t\tres={}\n\t\tt=self.browse(cr,uid,ids,context=None\n\t\tfor h in t:\n\t\t\tres[h.id]=0\n\t\treturn res\n" 
					field="'$field' : fields.function(_get_$field,type='integer',string='$display', store=False),"


			esac	
			if [[ $fields == "" ]]; then 
				fields="\t\t$field"
			else
				fields="$fields\n\t\t$field"
			fi
		fi
		echo ""
	done
	
	modelpython="class ${name}_$model(osv.osv):$functions\n\t_name = '$name.$model'\n\t_columns = {\n$fields\n\t}\n${name}_$model()\n\n"
	echo -e "[1;37m$modelpython[0m"
	python=$python$modelpython

	recordform="$recordform$fieldsxml\n\t\t</group></sheet></form></field></record>\n\n"
	recordtree="$recordtree$fieldsxml\n\t\t</tree></field></record>\n\n"
	actionxml=" <record model=\"ir.actions.act_window\" id=\"action_${name}_$model\">\n\t<field name=\"name\">$model</field>\n\t<field name=\"res_model\">$name.$model</field>\n\t<field name=\"view_type\">form</field>\n\t<field name=\"view_mode\">tree,form</field>\n</record>\n\n"
	menuxml="<menuitem name=\"$model\" id=\"menu_${name}_$model\" action=\"action_${name}_$model\" parent=\"menu_${name}_management\"/>\n\n"

	xml=$xml$recordform$recordtree$actionxml$menuxml
done

xml="$xml</data></openerp>"
#echo -e "$python"
#echo -e "$xml"

# Creation:

mkdir $name
echo -e "$python" > $name/$name.py
echo -e "$xml" > $name/view_$name.xml

echo "import $name" > $name/__init__.py

cat << EOF > $name/__openerp__.py
{
        "name" : "$name",
        "version" : "0.1",
        "author" : "Model Generator",
        "website" : "http://openerp.com",
        "category" : "Unknown",
        "description": """ Module generated change description """,
        "depends" : ['base'],
        "init_xml" : [ ],
        "demo_xml" : [ ],
        "update_xml" : ['view_$name.xml'],
        "installable": True
}
EOF

