

# Jquery Notes

jquery selectors:  
https://www.w3schools.com/jquery/jquery_selectors.asp

Jquery uses css selectors:  
https://www.w3schools.com/cssref/css_selectors.asp


Jquery select elements by class and attributes
```
$("li.chapter[data-level='1']")
$("li.chapter[hidden]")
```

Can hide elements using the  hidden attribute
```
<div hidden> </div>
```

Remove attributes 
```
$("a").removeAttr("href");
```

Using `$()[0]` or `$().get(0)` to select specific elemnts removes Jquery methods. To get them back use
```
$($("li.chapter[data-level='1']").get(0))
```

Set an attribute without a value
```
$($("li.chapter[data-level='1']").get(0)).attr("hidden", "")
```


Looping across Jquery items:
```
$( "li" ).each(function( index ) {
  console.log( index + ": " + $( this ).text() );
});
```


Check if variable is defined
```
if(typeof page_name != 'undefined')
```




Get parents  (recursively)
```
var _parent = $("li.chapter[data-level='1.1']").parents("li")
var _siblings = $("li.chapter[data-level='1.1']").siblings("li")
var _children =  $("li.chapter[data-level='1.1']").find("li")

_parent.add(_siblings).add(_children)
```


# Issues

Data-levels not being nested

Internal links to reference on same page not working

Intra page links not working

Index page appearing twice

Index page not appearing at all

Data-levels not being unique assigned

svg's  not being displayed



