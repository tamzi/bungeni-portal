YAHOO.util.Event.onContentReady("datefields2", function () {

        function onButtonClick() {

            /*
                 Create a Calendar instance and render it into the body 
                 element of the Overlay.
            */

            var oCalendar = new YAHOO.widget.Calendar("buttoncalendar2", oCalendarMenu.body.id);

            oCalendar.render();



            /* 
                Subscribe to the Calendar instance's "changePage" event to 
                keep the Overlay visible when either the previous or next page
                controls are clicked.
            */

            oCalendar.changePageEvent.subscribe(function () {
                
                window.setTimeout(function () {

                    oCalendarMenu.show();
                
                }, 0);
            
            });


            /*
                Subscribe to the Calendar instance's "select" event to 
                update the Button instance's label when the user
                selects a date.
            */

            oCalendar.selectEvent.subscribe(function (p_sType, p_aArgs) {

				var aDate,
					nMonth,
					nDay,
					nYear;

				if (p_aArgs) {
					
					aDate = p_aArgs[0][0];

					nMonth = aDate[1];
					nDay = aDate[2];
					nYear = aDate[0];

					oButton.set("label", (nMonth + "/" + nDay + "/" + nYear));


					// Sync the Calendar instance's selected date with the date form fields

					YAHOO.util.Dom.get("month2").selectedIndex = (nMonth - 1);
					YAHOO.util.Dom.get("day2").selectedIndex = (nDay - 1);
					YAHOO.util.Dom.get("year2").value = nYear;

				}
				
				oCalendarMenu.hide();
            
            });


            /*
                 Unsubscribe from the "click" event so that this code is 
                 only executed once
            */

            this.unsubscribe("click", onButtonClick);
        
        }


		var oDateFields = YAHOO.util.Dom.get("datefields2");
			oMonthField = YAHOO.util.Dom.get("month2"),
			oDayField = YAHOO.util.Dom.get("day2"),
			oYearField = YAHOO.util.Dom.get("year2");


		/*
			 Hide the form fields used for the date so that they can be replaced by the 
			 calendar button.
		*/

		oMonthField.style.display = "none";
		oDayField.style.display = "none";
		oYearField.style.display = "none";


        // Create a Overlay instance to house the Calendar instance

        var oCalendarMenu = new YAHOO.widget.Overlay("calendarmenu", { visible: false });


        // Create a Button instance of type "menu"

        var oButton = new YAHOO.widget.Button({ 
                                        type: "menu", 
                                        id: "calendarpicker2", 
                                        label: "Choose A Date", 
                                        menu: oCalendarMenu, 
                                        container: "datefields2" });


		oButton.on("appendTo", function () {
		
			/*
				 Create an empty body element for the Overlay instance in order 
				 to reserve space to render the Calendar instance into.
			*/
	
			oCalendarMenu.setBody("&#32;");
	
			oCalendarMenu.body.id = "calendarcontainer2";
	
	
			// Render the Overlay instance into the Button's parent element
	
			oCalendarMenu.render(this.get("container"));
		
		});


        /*
            Add a listener for the "click" event.  This listener will be
            used to defer the creation the Calendar instance until the 
            first time the Button's Overlay instance is requested to be displayed
            by the user.
        */        

        oButton.on("click", onButtonClick);
    
    });

