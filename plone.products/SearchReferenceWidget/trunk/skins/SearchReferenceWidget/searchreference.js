function SearchReference(name, displaytext, savetext) {
    this.name = name;   // id of frame, and name of JS variable set to this instance.
    this.element = document.getElementById(name);
    this.displaytext = document.getElementById(displaytext);
    this.savetext = document.getElementById(savetext);
    this.single = false;
    this.windowTitle='Select links';
    this.batch_size=100;
    
    this.initialize = function(editor, drawertool) {
        this.editor = editor;
        this.drawertool = drawertool;
    };

    this.addReference = function(uid, title) {
        // Add the specified reference to the list of references.
        //alert("Add reference: "+uid+", "+title);
        if (this.single) {
            this.removeAllReferences();
        }
        var el = document.createElement("div");
        var remove = document.createElement("a");
        var delimage = document.createElement("img");
        delimage.src = "delete_icon.gif";
        remove.appendChild(document.createTextNode('remove'));
        remove.href = "#";
        var handler=this;
        removeit = function() {
            handler.removeReference(uid);
            return false;
        };
        remove.onclick = removeit;
        el.appendChild(document.createTextNode('\u00a0'));
        el.appendChild(document.createTextNode(title));
        el.appendChild(document.createTextNode(' '));
        el.appendChild(remove);
        el.id = uid;
        this.displaytext.appendChild(el);

        if (this.single) {
            this.savetext.value = uid;
        } else {
            var save = this.savetext.value.split(/\r?\n/);
            save.push(uid);
            this.savetext.value = save.join('\n');
        }
    };

    this.removeAllReferences = function() {
        var divs = this.displaytext.childNodes;
        for (var i = divs.length-1; i >= 0; i--) {
            if (divs[i].nodeType==1) {
                this.displaytext.removeChild(divs[i]);
            }
        }
        this.savetext.value = '';
    }
    
    this.removeReference = function(uid) {
        var divs = this.displaytext.childNodes;
        var save = new Array();
        for (var i = divs.length-1; i >= 0; i--) {
            if (divs[i].nodeType==1) {
                var UID = divs[i].id;
                if (UID==uid) {
                    this.displaytext.removeChild(divs[i]);
                } else {
                    save.push(UID);
                }
            }
        }
        save.reverse();
        this.savetext.value = save.join('\n');
    };

    
    // Live search stuff
    this.allowed_types = []
    this.target_node = null
    this.hits = 0;

    // constants for better compression
    var _cssQuery = cssQuery;
    var _registerEventListener = registerEventListener;

	this.setTarget = function(event) {
	  u = 'typedlivesearch_reply?toolname='+this.name
	  if (this.portal_type != null) {
	  	sel_type = this.portal_type.value;
	  } else {
	    sel_type = '';
	  }
	  u += '&portal_type='+sel_type;
	  allowed = this.allowed_types
	  for (i=0; i<allowed.length; i++) {
	  	u += '&allowed_types:list=' + allowed[i]
	  }
	  u += '&q=';
	  this.target_node.value=u;
	  if (this.hits==0) {
	  	this.hits = 1;
	  	return; //ignore first one as its not done by user
	  } else {
	  	this.input_node.focus(); //should activate live search
	  }
	  return u;
  
	}

    function _isform($node) {
        // return true if the node is a form. used for findContainer in _setup.
        //DJJ: don't rely on single form
        if ($node.tagName && ($node.tagName == 'FORM' || $node.tagName == 'form') ||
            $node.className && ($node.className == 'LSBox')) {
            return true;
        }
        return false;
    };


    $thisobj = this
    
    this._setup = function($inputnode, $number) {
        // set up all the event handlers and other stuff
        this.target_node = $inputnode;

        var $portal_type = _cssQuery("select[name=portal_type]", this.form);
        if ($portal_type.length == 1) {
            $portal_type = $portal_type[0];
        } else {
            $portal_type = null;
        }
        this.portal_type = $portal_type;

        var $node = _cssQuery("input.portlet-search-gadget", this.form);
        if ($node.length == 1) {
            $node = $node[0];
        } else {
            $node = null;
        }
        this.input_node = $node;
        
        f = this.setTarget.bind(this);
        //f = function() { this.setTarget(); }
        if (this.portal_type != null) {
        	_registerEventListener(this.portal_type, "change", f);
        }
        f();

	}

    this._init = function() {
        if (!W3CDOM)
            return; // the browser doesn't support enough functions
        // find all search fields and set them up
        this.form = this.displaytext.parentNode
        var $gadgets = _cssQuery("input.querytarget", this.form);
        for (var i=0; i < $gadgets.length; i++) {
            this._setup($gadgets[i], i);
        }
    };

	/*registerPloneFunction(_init);*/
	_registerEventListener(window, "load", this._init.bind(this)); /*DJJ: need to run after widgets loaded*/

}











 Function.prototype.bind = function(obj) {
  var method = this,
   temp = function() {
    return method.apply(obj, arguments);
   };
 
  return temp;
 } 