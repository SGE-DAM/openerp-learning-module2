{
        "name" : "championship",
        "version" : "0.1",
        "author" : "Castillo",
        "website" : "http://openerp.com",
        "category" : "Unknown",
        "description": """ Module for a Championship """,
        "depends" : ['base','report_webkit','sale'],
        "init_xml" : [ ],
        "demo_xml" : [ ],
        "update_xml" : ['championship_view.xml','equips.xml','jugadors/val.xml', 'jugadors/atl.xml',
			'report/header_championship.xml',
			'champion_report.xml'],
        "installable": True
}
