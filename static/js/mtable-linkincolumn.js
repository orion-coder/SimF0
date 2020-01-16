(function($){

    $.fn.linkincolumn = function(args) {

        $(this).each(function(e){
            var table = $(this);
            var tbody = table.find('tbody').not("."+args.exceptLink);
				args = parseArgs(table, args);
				if(table.find('tbody').length > 0){
					applyLinks(tbody, args.targetColumn, args.targetLink);
				}
        });
    
        function parseArgs(table, args) {
            if(typeof args == "undefined") args = [];
            if(typeof args.targetColumn !== "undefined" && args.targetColumn >= 0) {
                args.targetColumn = parseInt(args.targetColumn);
            }else{
                args.targetColumn = 0;
            }
            return args;
        }

        function applyLinks(block, targetColumn, targetLink) {
            block.find('tr').each(function(i) {
					 var NewName = '<a href="'+targetLink+$(this).children().eq(targetColumn).text()+'" target="_blank">'+$(this).children().eq(targetColumn).text()+'</a>';
					 $(this).children().eq(targetColumn).html(NewName);
            });
        }
        return this;
    }
})(jQuery);

