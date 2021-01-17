$(document).ready(function() {
    
    var callback = function(entries, observer) { 
        entries.forEach(entry => {
            var dl = $(entry.target).attr("data-link-index");
            var elements = $("li[data-link-index='" + dl + "']").children("ul").children("li");
            if(entry.isIntersecting){
                elements.removeAttr("hidden");
            } else {
                elements.attr("hidden", "");
            }
        });
      };
    
    var observer = new IntersectionObserver(callback, {});
   
    $("div[data-link-index]").each( function(index){
        observer.observe(this);    
    })
    $("section[data-link-index]").each( function(index){
        observer.observe(this);    
    })
});




