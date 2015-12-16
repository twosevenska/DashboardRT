	$('#dir-inbox-table').bootstrapTable({
 	    columns: [{
 	        field: 'ticketName',
 	        title: ''
 	    }, {
			field: 'actions',
			title: ''
		}],
 	    data: [{
 	        ticketName: 'Futurama',
 	    }, {
 	        ticketName: 'Firefly',
 	    }]
 	});
	
		$('#stalled-table').bootstrapTable({
 	    columns: [{
 	        field: 'ticketName',
 	        title: ''
 	    }, {
			field: 'actions',
			title: ''
		}],
 	    data: [{
 	        ticketName: 'Futurama',
 	    }, {
 	        ticketName: 'Firefly',
 	    }]
 	});
	
	$('#in-table').bootstrapTable({
 	    columns: [{
 	        field: 'ticketName',
 	        title: ''
 	    }, {
			field: 'actions',
			title: ''
		}],
 	    data: [{
 	        ticketName: 'Futurama',
 	    }, {
 	        ticketName: 'Firefly',
 	    }]
 	});
	
	$('#active-table').bootstrapTable({
 	    columns: [{
 	        field: 'ticketName',
 	        title: ''
 	    }, {
			field: 'actions',
			title: ''
		}],
 	    data: [{
 	        ticketName: 'Futurama',
 	    }, {
 	        ticketName: 'Firefly',
 	    }]
 	});
	
	$('#done-table').bootstrapTable({
 	    columns: [{
 	        field: 'ticketName',
 	        title: ''
 	    }, {
			field: 'actions',
			title: ''
		}],
 	    data: [{
 	        ticketName: 'Futurama',
 	    }, {
 	        ticketName: 'Firefly',
 	    }]
 	});
	
	window.operateEvents = {
        'click .like': function (e, value, row) {
            alert('You click like action, row: ' + JSON.stringify(row));
        },
        'click .remove': function (e, value, row) {
            alert('You click remove action, row: ' + JSON.stringify(row));
        }
    };
	
	
    function operateFormatter(value, row, index) {
        return [
            '<div class="pull-left">',
            '<a href="https://github.com/wenzhixin/' + value + '" target="_blank">' + value + '</a>',
            '</div>',
            '<div class="pull-right">',
            '<a class="like" href="javascript:void(0)" title="Like">',
            '<i class="glyphicon glyphicon-heart"></i>',
            '</a>  ',
            '<a class="remove" href="javascript:void(0)" title="Remove">',
            '<i class="glyphicon glyphicon-remove"></i>',
            '</a>',
            '</div>'
        ].join('');
    }
	
	