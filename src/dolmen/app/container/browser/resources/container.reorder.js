/*
// TableDnD jQuery plugin
// Functionality: S o r t a b l e for native HTML tables
// Depends on: jQuery Base
//
*/
$(document).ready(
	function () {
		// prerequisites - give out id's
		$('table.orderable').attr('id', 'folderlisting');
		
		var idNum = 0;
		$('table.orderable > tbody tr').each(function(){
			$(this).attr('id', 'order-id_' + idNum);
			idNum++;
		}); 
		
	    // Initialise the table
	    $("table.orderable").tableDnD({
	    	onDragClass: "dragging",
	      	serializeRegexp: /[^\-]*$/, // The regular expression to use to trim row IDs
	    	onDrop: function(table, row) {
	    	
	    		// transform serialized parameters into
	    		// javascript object
	    		var result = {};
	    		var rows = table.rows;
	    		result = [];
	    		for (var i=0; i<rows.length; i++) {
	    			var rowId = rows[i].id;
	    			if (rowId && rowId && table.tableDnDConfig && table.tableDnDConfig.serializeRegexp) {
	    				rowId = rowId.match(table.tableDnDConfig.serializeRegexp)[0];
	    			}	
	    			result[i] = rowId;
	    		}
	    		
	    		// adapt "odd" and "even" class declarations to new order
	    		var i = 0;
	    		$('table.orderable > tbody > tr').each(function(){
	    			if (i % 2 == 0){
	    				$(this).addClass('even');
	    				$(this).removeClass('odd');
	    			}else{
	    				$(this).addClass('odd');
	    				$(this).removeClass('even');
	    			}
	    			i++;
	    		})
	    		
	    		$.ajax({
            		url: updateContainerOrder,
            		dataType: "json",
            		data: {	newOrder: result }
            	});
            	
	    	}
	    });
	}
);


